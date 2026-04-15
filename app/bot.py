import os
import html
import logging
import asyncio
import functools
from typing import *

from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ChatType
from aiogram.filters import Command
from aiogram.types import Message, InlineQuery, ChosenInlineResult
from aiogram.exceptions import TelegramAPIError
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from klocmod import LocalizationsContainer, LanguageDictionary
from prometheus_client import start_http_server, Counter

import commands
import rand
import localization
from data.config import *
from util import Items, try_parse_int, try_extract_numbers, from_premium
from queryutil import InlineQueryResultsBuilder
from handler import InlineHandlersLoader


# INITIALIZATION

bot: Bot  # initialized in run()
dispatcher = Dispatcher()
localizations = LocalizationsContainer(localization.L)
inline_handlers = InlineHandlersLoader()
logger = logging.getLogger(__name__)

command_calls_counter = Counter("command_used", "Calls count of a command", ['handler'])
inline_counter = Counter("inline_used", "Inline queries count")
chosen_inline_res_counter = Counter("inline_result_chosen", "Count of times when inline result was chosen", ['handler'])
password_length_counter = Counter("passwords_generated", "Count of generated passwords split by length", ['length'])


# DECORATORS

def reply_if_group(**kwargs) -> callable:
    """
    A decorator to convert a synchronous function with facilities for localization into an asynchronous message handler.

    Decorate a function with signature 'Message, LanguageDictionary -> str' into an asynchronous message handler that
    sends some text message back to the user. If the bot is in a group chat, the message will be sent as a reply to the
    original message. In private chats, it will be sent just like a regular message.

    :param kwargs: any parameters that must be applied to the 'sendMessage' Telegram API method
    :return: asynchronous message handler as a decorator
    """
    def generator(func: Callable[[Message, LanguageDictionary], str]) -> Callable[[Message], Awaitable]:
        @functools.wraps(func)
        async def wrapper(message: Message) -> None:
            lang = localizations.get_lang(message.from_user.language_code)
            text = func(message, lang)
            if message.chat.type in (ChatType.GROUP, ChatType.SUPERGROUP):
                await message.reply(text, **kwargs)
            else:
                await bot.send_message(message.chat.id, text, **kwargs)
        del wrapper.__wrapped__  # prevent inspect.iscoroutinefunction from unwrapping to the sync func
        return wrapper
    return generator


# MESSAGE HANDLERS

@dispatcher.message(Command('start', 'help'))
@reply_if_group(parse_mode="Markdown")
def get_help(_: Message, lang: LanguageDictionary) -> str:
    command_calls_counter.labels("help").inc()
    return lang['help'].format(*[DEFAULT_PASSWORD_LENGTH]*2)


@dispatcher.message(Command('coin', 'flip_coin'))
@reply_if_group()
def flip_coin(message: Message, lang: LanguageDictionary) -> str:
    command_calls_counter.labels("flip_coin").inc()
    return rand.one_out_of_two(lang['heads'], lang['tails'], from_premium(message))


@dispatcher.message(Command('yesno', 'yes_or_no'))
@reply_if_group()
def yes_or_no(message: Message, lang: LanguageDictionary) -> str:
    command_calls_counter.labels("yes_or_no").inc()
    yes = lang['yes'].capitalize() + '!'
    no = lang['no'].capitalize() + '.'
    return rand.one_out_of_two(yes, no, from_premium(message))


@dispatcher.message(Command('num', 'number'))
@reply_if_group(parse_mode="Markdown")
def get_random_number(message: Message, lang: LanguageDictionary) -> str:
    command_calls_counter.labels("number").inc()

    wrong_text_message = "{}: `/number [{}] <{}>`".format(lang['usage'], lang['from'], lang['to'])

    text = _get_args(message)
    numbers = try_extract_numbers(text)
    if not numbers:
        if not message.reply_to_message:
            return wrong_text_message
        numbers = try_extract_numbers(message.reply_to_message.text)
        if not numbers:
            return wrong_text_message

    use_premium_random = from_premium(message)
    if len(numbers) > 1:
        rand_num = rand.between(numbers[0], numbers[1], use_premium_random)
    else:
        rand_num = rand.maximum(numbers[0], use_premium_random)
    return str(rand_num)


@dispatcher.message(Command('list'))
@reply_if_group(parse_mode="HTML")
def get_random_item(message: Message, lang: LanguageDictionary) -> str:
    command_calls_counter.labels("list").inc()

    wrong_text_message = "{} <code>/list {} 1, {} 2, {} 3...</code>".format(
        lang['usage'], lang['item'], lang['item'], lang['item'])

    text = _get_args(message)
    if not text:
        if not message.reply_to_message:
            return wrong_text_message
        text = message.reply_to_message.text

    items = Items(text)
    if items.acceptable:
        item = rand.item_from_list(items.list, from_premium(message))
        return html.escape(item)
    else:
        return wrong_text_message


@dispatcher.message(Command('seq', 'password', 'sequence'))
@reply_if_group()
def get_password(message: Message, lang: LanguageDictionary) -> str:
    command_calls_counter.labels("seq").inc()
    generator = functools.partial(rand.strong_password,
                                  extra_chars=PASSWORD_EXTRA_CHARS,
                                  max_tries=MAX_PASSWORD_GENERATION_TRIES)
    return _get_password(_get_args(message), lang, generator)


@dispatcher.message(Command('seqc', 'cseq', 'passwd'))
@reply_if_group()
def get_password_conservative(message: Message, lang: LanguageDictionary) -> str:
    command_calls_counter.labels("seqc").inc()
    generator = functools.partial(rand.strong_password,
                                  max_tries=MAX_PASSWORD_GENERATION_TRIES)
    return _get_password(_get_args(message), lang, generator)


@dispatcher.message(Command('hex'))
@reply_if_group()
def get_hex_password(message: Message, lang: LanguageDictionary) -> str:
    command_calls_counter.labels("hex").inc()
    return _get_password(_get_args(message), lang, rand.hex_password)


def _get_password(args: str, lang: LanguageDictionary, generator: Callable[[int], str]) -> str:
    length = try_parse_int(args) if args else DEFAULT_PASSWORD_LENGTH
    if length and MIN_PASSWORD_LENGTH <= length <= MAX_PASSWORD_LENGTH:
        password_length_counter.labels(length).inc()
        return generator(length)
    else:
        return lang['password_length_invalid'].format(MIN_PASSWORD_LENGTH, MAX_PASSWORD_LENGTH)


@dispatcher.message(Command('uuid'))
@reply_if_group()
def get_uuid(message: Message, lang: LanguageDictionary) -> str:
    command_calls_counter.labels("uuid").inc()
    return rand.uuid()


def _get_args(message: Message) -> str:
    """Extract arguments after the command from message text."""
    parts = (message.text or '').split(maxsplit=1)
    return parts[1] if len(parts) > 1 else ''


# INLINE HANDLER

@dispatcher.inline_query()
async def show_inline_suggestions(query: InlineQuery) -> None:
    inline_counter.inc()

    lang = localizations.get_lang(query.from_user.language_code)
    builder = InlineQueryResultsBuilder()

    for handler in inline_handlers.match_handlers(query.query):
        builder.new_article(res_id=handler.name,
                            title=lang[handler.name + '_title'],
                            description=handler.get_description(query.query, lang),
                            text=handler.get_text(query.query, lang, from_premium(query)),
                            parse_mode=handler.parse_mode)

    try:
        await bot.answer_inline_query(query.id, builder.build_list(), cache_time=1, is_personal=True)
    except TelegramAPIError as err:
        err_msg = str(err) + '\n'
        for i in builder.build_list():
            err_msg += '(description="{}", text="{}")\n'.format(i.description, i.input_message_content.message_text)
        logger.exception(err_msg)


@dispatcher.chosen_inline_result()
async def inc_counter_of_chosen_result(chosen_inline_query: ChosenInlineResult) -> None:
    chosen_inline_res_counter.labels(chosen_inline_query.result_id).inc()


# ENTRY POINT

async def _start_polling() -> None:
    async def delete_webhook() -> None:
        await bot.delete_webhook(drop_pending_updates=True)
    dispatcher.startup.register(delete_webhook)
    dispatcher.startup.register(commands.gen_startup_hook(bot, localizations))
    await dispatcher.start_polling(bot)


async def _start_webhook() -> None:
    async def set_webhook() -> None:
        await bot.set_webhook(f"https://{HOST}:{SERVER_PORT}/{NAME}/{TOKEN}", drop_pending_updates=True)
    dispatcher.startup.register(set_webhook)
    dispatcher.startup.register(commands.gen_startup_hook(bot, localizations))

    app = web.Application()
    SimpleRequestHandler(dispatcher=dispatcher, bot=bot).register(app, path=f"/{NAME}/{TOKEN}")
    setup_application(app, dispatcher, bot=bot)

    runner = web.AppRunner(app)
    try:
        await runner.setup()
        if SOCKET_TYPE == 'TCP':
            site = web.TCPSite(runner, host=APP_HOST, port=int(APP_PORT))
        elif SOCKET_TYPE == 'UNIX':
            os.umask(0o137)
            site = web.UnixSite(runner, path=UNIX_SOCKET)
        else:
            raise ValueError("The value of the SOCKET_TYPE environment variable is invalid!")
        await site.start()
        await asyncio.Event().wait()
    finally:
        await runner.cleanup()


async def run() -> None:
    global bot
    session = AiohttpSession(proxy=PROXY) if PROXY else None
    bot = Bot(TOKEN, session=session)
    try:
        await (_start_polling() if DEBUG else _start_webhook())
    finally:
        if bot.session:
            await bot.session.close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG if DEBUG else logging.INFO)
    start_http_server(METRICS_PORT)
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        pass
