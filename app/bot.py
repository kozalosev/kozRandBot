import os
import random
import asyncio
import logging
import functools
from typing import *

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import Message, InlineQuery, ChosenInlineResult
from aiogram.utils.markdown import quote_html
from aiogram.utils.exceptions import TelegramAPIError
from klocmod import LocalizationsContainer, LanguageDictionary
from prometheus_client import start_http_server, Counter

import rand
import localization
from data.config import *
from util import Items, try_parse_int, try_extract_numbers
from queryutil import InlineQueryResultsBuilder
from handler import InlineHandlersLoader


# INITIALIZATION

bot = Bot(TOKEN)
dispatcher = Dispatcher(bot)
localizations = LocalizationsContainer(localization.L)
inline_handlers = InlineHandlersLoader()
logger = logging.getLogger(__name__)

command_calls_counter = Counter("command_used", "Calls count of a command", ['handler'])
inline_counter = Counter("inline_used", "Inline queries count")
chosen_inline_res_counter = Counter("inline_result_chosen", "Count of times when inline result was chosen", ['handler'])


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
            if types.ChatType.is_group_or_super_group(message.chat):
                await message.reply(text, **kwargs)
            else:
                await bot.send_message(message.chat.id, text, **kwargs)
        return wrapper
    return generator


# MESSAGE HANDLERS

@dispatcher.message_handler(commands=['start', 'help'])
@reply_if_group(parse_mode="Markdown")
def get_help(_: Message, lang: LanguageDictionary) -> str:
    command_calls_counter.labels("help").inc()
    return lang['help'].format(DEFAULT_PASSWORD_LENGTH)


@dispatcher.message_handler(commands=['coin', 'flip_coin'])
@reply_if_group()
def flip_coin(_: Message, lang: LanguageDictionary) -> str:
    command_calls_counter.labels("flip_coin").inc()
    return rand.one_out_of_two(lang['heads'], lang['tails'])


@dispatcher.message_handler(commands=['yesno', 'yes_or_no'])
@reply_if_group()
def yes_or_no(_: Message, lang: LanguageDictionary) -> str:
    command_calls_counter.labels("yes_or_no").inc()
    return rand.one_out_of_two(lang['yes'].capitalize() + '!', lang['no'].capitalize() + '.')


@dispatcher.message_handler(commands=['num', 'number'])
@reply_if_group(parse_mode="Markdown")
def get_random_number(message: Message, lang: LanguageDictionary) -> str:
    command_calls_counter.labels("number").inc()

    wrong_text_message = "{}: `/number [{}] <{}>`".format(lang['usage'], lang['from'], lang['to'])

    text = message.get_args()
    numbers = try_extract_numbers(text)
    if not numbers:
        if not message.reply_to_message:
            return wrong_text_message
        numbers = try_extract_numbers(message.reply_to_message.text)
        if not numbers:
            return wrong_text_message

    if len(numbers) > 1:
        rand_num = rand.between(numbers[0], numbers[1])
    else:
        rand_num = rand.maximum(numbers[0])
    return str(rand_num)


@dispatcher.message_handler(commands=['list'])
@reply_if_group(parse_mode="HTML")
def get_random_item(message: Message, lang: LanguageDictionary) -> str:
    command_calls_counter.labels("list").inc()

    wrong_text_message = "{} <code>/list {} 1, {} 2, {} 3...</code>".format(
        lang['usage'], lang['item'], lang['item'], lang['item'])

    text = message.get_args()
    if not text:
        if not message.reply_to_message:
            return wrong_text_message
        text = message.reply_to_message.text

    items = Items(text)
    if items.acceptable:
        return quote_html(random.choice(items.list))
    else:
        return wrong_text_message


@dispatcher.message_handler(commands=['seq', 'password', 'sequence'])
@reply_if_group()
def get_password(message: Message, lang: LanguageDictionary) -> str:
    command_calls_counter.labels("seq").inc()

    text = message.get_args()
    length = try_parse_int(text) if text else DEFAULT_PASSWORD_LENGTH
    if length and MIN_PASSWORD_LENGTH <= length <= MAX_PASSWORD_LENGTH:
        return rand.strong_password(length, PASSWORD_EXTRA_CHARS, MAX_PASSWORD_GENERATION_TRIES)
    else:
        return lang['password_length_invalid'].format(MIN_PASSWORD_LENGTH, MAX_PASSWORD_LENGTH)


@dispatcher.message_handler(commands=['seqc', 'cseq', 'passwd'])
@reply_if_group()
def get_password(message: Message, lang: LanguageDictionary) -> str:
    command_calls_counter.labels("seqc").inc()

    text = message.get_args()
    length = try_parse_int(text) if text else DEFAULT_PASSWORD_LENGTH
    if length and MIN_PASSWORD_LENGTH <= length <= MAX_PASSWORD_LENGTH:
        return rand.strong_password(length, max_tries=MAX_PASSWORD_GENERATION_TRIES)
    else:
        return lang['password_length_invalid'].format(MIN_PASSWORD_LENGTH, MAX_PASSWORD_LENGTH)


# INLINE HANDLER

@dispatcher.inline_handler(lambda query: True)
async def show_inline_suggestions(query: InlineQuery) -> None:
    inline_counter.inc()

    lang = localizations.get_lang(query.from_user.language_code)
    builder = InlineQueryResultsBuilder()

    for handler in inline_handlers.match_handlers(query.query):
        builder.new_article(res_id=handler.name,
                            title=lang[handler.name + '_title'],
                            description=handler.get_description(query.query, lang),
                            text=handler.get_text(query.query, lang),
                            parse_mode=handler.parse_mode)

    try:
        await bot.answer_inline_query(query.id, builder.build_list(), cache_time=1, is_personal=True)
    except TelegramAPIError as err:
        err_msg = str(err) + '\n'
        for i in builder.build_list():
            err_msg += '(description="{}", text="{}")\n'.format(i.description, i.input_message_content.message_text)
        logger.exception(err_msg)


@dispatcher.chosen_inline_handler()
async def inc_counter_of_chosen_result(chosen_inline_query: ChosenInlineResult) -> None:
    chosen_inline_res_counter.labels(chosen_inline_query.result_id).inc()


# ENTRY POINT

if __name__ == '__main__':
    start_http_server(METRICS_PORT)
    if DEBUG:
        logging.basicConfig(level=logging.DEBUG)
        asyncio.get_event_loop().run_until_complete(bot.delete_webhook())
        executor.start_polling(dispatcher, skip_updates=True)
    else:
        async def set_webhook_async(_: Dispatcher) -> None:
            await bot.set_webhook(f"https://{HOST}:{SERVER_PORT}/{NAME}/{TOKEN}")

        os.umask(0o137)  # rw-r----- for the Unix socket
        executor.start_webhook(dispatcher, path=UNIX_SOCKET, webhook_path=f"/{NAME}/{TOKEN}",
                               on_startup=set_webhook_async, skip_updates=True)
