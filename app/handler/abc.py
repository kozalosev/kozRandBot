"""Abstract base classes and mix-ins that are used throughout the system and by implementers."""

import re
from abc import ABC, abstractmethod
from klocmod import LanguageDictionary

from .util import classproperty


__all__ = ['InlineHandler', 'Universal', 'HTML', 'Markdown']


class InlineHandler(ABC):
    """
    Base class for all inline handlers. Your class must extend this one to
    let the loader discover it.

    The key idea is that all handlers can answer whether they're able to
    handle the string (query) or not. If they can, they must return a
    result when the 'get_text' method will be invoked.

    If a handler wants to use HTML or Markdown, it must set the corresponding
    parse mode via the 'parse_mode' class variable (or better use 'HTML' and
    'Markdown' mix-in classes). Note, however, that handlers must escape HTML
    entities in the input query by themselves! Use the 'handler.escape_html'
    function for that. Telegram flavored Markdown is much harder to escape
    properly, so don't use it if user input is involved.

    Also, implementations can override the 'get_description' method. By default,
    it uses the localization system with key '{name}_description' where name is
    the name of a class in snake_case without words "inline" and "handler" at
    the end. Titles are fetched from the system with keys following the pattern
    '{name}_title'.
    """

    # Marker used instead of 'issubclass' to search for descendants of this class.
    # See: https://stackoverflow.com/a/11461574
    __message_handler__ = True

    parse_mode: str = None

    @classmethod
    @abstractmethod
    def can_process(cls, query: str) -> bool:
        pass

    @abstractmethod
    def get_text(self, query: str, lang: LanguageDictionary) -> str:
        pass

    def get_description(self, query: str, lang: LanguageDictionary) -> str:
        return lang[self.name + '_description']

    @classproperty
    @classmethod
    def name(cls) -> str:
        """
        Return the name of the class in snake_case.

        May be useful to use this string as a key for localization dictionary,
        for example.
        """

        def to_snake_case(name):
            """https://stackoverflow.com/a/1176023"""
            s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
            return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

        name = cls.__name__
        if name.endswith("Handler"):
            name = name[:-len("handler")]
        if name.endswith("Inline"):
            name = name[:-len("inline")]
        return to_snake_case(name)


class Universal:
    """Mix-in class that's used for processors that can handle any text."""
    @staticmethod
    def can_process(_: str) -> bool:
        return True


class HTML:
    """Mix-in class that enables the use of HTML tags."""
    parse_mode = "HTML"


class Markdown:
    """Mix-in class that enables the use of Markdown markup language."""
    parse_mode = "Markdown"
