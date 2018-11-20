import os
import re
import random
import asyncio
import logging
import functools
from typing import *

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import Message, InlineQuery
from aiogram.utils.markdown import quote_html
from aiogram.utils.exceptions import TelegramAPIError
from klocmod import LocalizationsContainer, LanguageDictionary

from data.config import *
from util import Items, try_parse_int, try_extract_numbers
from queryutil import InlineQueryResultsBuilder
import rand
import localization


# INITIALIZATION

bot = Bot(TOKEN)
dispatcher = Dispatcher(bot)
localizations = LocalizationsContainer(localization.L)
logger = logging.getLogger(__name__)


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
    return lang['help']


@dispatcher.message_handler(commands=['coin', 'flip_coin'])
@reply_if_group()
def flip_coin(_: Message, lang: LanguageDictionary) -> str:
    return rand.one_out_of_two(lang['heads'], lang['tails'])


@dispatcher.message_handler(commands=['yesno', 'yes_or_no'])
@reply_if_group()
def yes_or_no(_: Message, lang: LanguageDictionary) -> str:
    return rand.one_out_of_two(lang['yes'].capitalize() + '!', lang['no'].capitalize() + '.')


@dispatcher.message_handler(commands=['num', 'number'])
@reply_if_group(parse_mode="Markdown")
def get_random_number(message: Message, lang: LanguageDictionary) -> str:
    wrong_text_message = "%s: `/number [%s] <%s>`" % (lang['usage'], lang['from'], lang['to'])

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
    wrong_text_message = "%s <code>/list %s 1, %s 2, %s 3...</code>" % (
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
    text = message.get_args()
    length = try_parse_int(text) if text else DEFAULT_PASSWORD_LENGTH
    if length and 6 <= length <= 2048:
        return rand.password(length)
    else:
        return lang['password_length_invalid']


# INLINE HANDLER

@dispatcher.inline_handler(lambda query: True)
async def show_inline_suggestions(query: InlineQuery) -> None:
    items = Items(query.query)

    test_range = re.match(r"^([0-9]+),?\s+([0-9]+)$", query.query)
    test_question = query.query[-1] == '?' if len(query.query) > 0 else False
    test_max = try_parse_int(query.query)

    lang = localizations.get_lang(query.query)
    builder = InlineQueryResultsBuilder()

    if test_question:
        yes_no_result = rand.one_out_of_two(lang['yes'], lang['no'])
        message = lang['yes_no_message'] % (quote_html(query.query), quote_html(yes_no_result))
        builder.new_article(lang['yes_no_title'], description=lang['yes_no_description'], text=message,
                            parse_mode="HTML")
    if items.acceptable:
        items_list = [quote_html(s) for s in items.list]
        message = lang['rand_item_message'] % (query.query, random.choice(items_list))
        builder.new_article(lang['rand_item_title'], description=lang['rand_item_description'], text=message,
                            parse_mode="HTML")

    if test_range:
        min_val, max_val = int(test_range.group(1)), int(test_range.group(2))
        message = lang['rand_num_message'] % (min_val, max_val, rand.between(min_val, max_val))
        description = lang['rand_num_description'] % (min_val, max_val)
        builder.new_article(lang['rand_num_title'], description=description, text=message, parse_mode="Markdown")
    elif test_max:
        message = lang['rand_num_from_zero_message'] % (test_max, rand.maximum(test_max))
        description = lang['rand_num_description'] % (1, test_max)
        builder.new_article(lang['rand_num_title'], description=description, text=message, parse_mode="Markdown")

    if test_max and 6 <= test_max <= 2048:
        pw_seq, pw_len = rand.password(test_max), test_max
    else:
        pw_seq, pw_len = rand.password(DEFAULT_PASSWORD_LENGTH), DEFAULT_PASSWORD_LENGTH
    builder.new_article(lang['password_title'], description=(lang['password_description'] % pw_len),
                        text=(lang['password_message'] % (pw_len, pw_seq)), parse_mode="HTML")

    builder.new_article(lang['flip_coin_title'], description=lang['flip_coin_description'],
                        text=rand.one_out_of_two(lang['heads'], lang['tails']))

    try:
        await bot.answer_inline_query(query.id, builder.build_list(), cache_time=1, is_personal=True)
    except TelegramAPIError as err:
        err_msg = str(err) + '\n'
        for i in builder.build_list():
            err_msg += '(description="%s", text="%s")\n' % (i.description, i.text)
        logger.exception(err_msg)


# ENTRY POINT

if __name__ == '__main__':
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
