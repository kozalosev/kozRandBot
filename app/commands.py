from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault
from klocmod import LocalizationsContainer
from typing import Callable, Coroutine


async def set_commands(bot: Bot, localizations: LocalizationsContainer) -> None:
    """Set a command list for all supported languages."""
    lang_commands = {name: dct['commands'] for name, dct in localizations if 'commands' in dct}
    default_scope = BotCommandScopeDefault()
    for lang, commands in lang_commands.items():
        cmds = [BotCommand(command=name, description=description) for name, description in commands.items()]
        await bot.set_my_commands(cmds, default_scope, lang)


def gen_startup_hook(bot: Bot, localizations: LocalizationsContainer) -> Callable[[], Coroutine]:
    async def func() -> None:
        await set_commands(bot, localizations)
    return func
