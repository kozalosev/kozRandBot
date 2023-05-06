from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeDefault
from klocmod import LocalizationsContainer
from typing import Callable, Coroutine


async def set_commands(bot: Bot, localizations: LocalizationsContainer) -> None:
    """Set a command list for all supported languages."""
    lang_commands = {name: dct['commands'] for name, dct in localizations if 'commands' in dct}
    default_scope = BotCommandScopeDefault()
    for lang, commands in lang_commands.items():
        cmds = [BotCommand(name, description) for name, description in commands.items()]
        await bot.set_my_commands(cmds, default_scope, lang)


def gen_startup_hook(bot: Bot, localizations: LocalizationsContainer) -> Callable[[Dispatcher], Coroutine]:
    async def func(_: Dispatcher) -> None:
        await set_commands(bot, localizations)
    return func
