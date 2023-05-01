"""
This module is intended to provide some useful builders for standard AIOGram types.

See also:
https://bitbucket.org/Kozalo/telegram-bots/src/1673bc274d1c67139a89965faf2ceaf353b0bd4e/botutils/builders.py?at=dev
"""

from aiogram.types import *
from typing import List


class InlineQueryResultsBuilder:
    """
    This class gives you a way to create a list of **InlineQueryResultArticle**s.

    UPD: this version was simplified and modified to support the chosen_inline_result metric.
    """

    def __init__(self):
        self._items = []

    def build_list(self) -> List[InlineQueryResultArticle]:
        """:returns: a copy of the collection."""
        return self._items.copy()

    def new_article(self, res_id: str, title: str, text: str,
                    parse_mode: str = None,
                    disable_web_page_preview: bool = None,
                    **kwargs) -> "InlineQueryResultsBuilder":
        """Creates a new article with specified parameters and appends it to the list."""
        input_message_content = InputTextMessageContent(text, parse_mode, disable_web_page_preview)
        obj = InlineQueryResultArticle(id=res_id, title=title, input_message_content=input_message_content,
                                       **kwargs)
        self._items.append(obj)
        return self
