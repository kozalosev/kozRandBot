"""
This module is intended to provide some useful builders for standard AIOGram types.

See also:
https://bitbucket.org/Kozalo/telegram-bots/src/1673bc274d1c67139a89965faf2ceaf353b0bd4e/botutils/builders.py?at=dev
"""

from aiogram.types import *


class InlineQueryResultsBuilder:
    """
    This class gives you a way to create a list of **InlineQueryResultArticle**s with incremental numeric ids starting
    from 1. Use `new_*()` methods to add items into an internal collection. Call `build_list()` to get its copy then.
    """

    def __init__(self):
        self._items = []
        self._counter = 0

    def _new_object(self, obj) -> "InlineQueryResultsBuilder":
        """Use this method to add a new item into the collection."""
        self._counter += 1
        self._items.append(obj)
        return self

    @property
    def empty(self) -> bool:
        """:returns *True* if the length of the collection is equal to zero."""
        return len(self._items) == 0

    def build_list(self) -> list:
        """:returns: a copy of the collection."""
        return self._items.copy()

    def new_article(self, title: str, text: str, parse_mode: str = None, disable_web_page_preview: bool = None,
                    **kwargs) -> "InlineQueryResultsBuilder":
        """Creates a new article with specified parameters and appends it to the list."""
        input_message_content = InputTextMessageContent(text, parse_mode, disable_web_page_preview)
        obj = InlineQueryResultArticle(id=str(self._counter), title=title, input_message_content=input_message_content,
                                       **kwargs)
        return self._new_object(obj)

    def new_photo(self, photo_id: str, **kwargs) -> "InlineQueryResultsBuilder":
        """Creates a new photo with specified parameters and appends it to the list."""
        obj = InlineQueryResultCachedPhoto(id=str(self._counter), photo_file_id=photo_id, **kwargs)
        return self._new_object(obj)

    def new_gif(self, gif_id: str, **kwargs) -> "InlineQueryResultsBuilder":
        """Creates a new gif with specified parameters and appends it to the list."""
        obj = InlineQueryResultCachedGif(id=str(self._counter), gif_file_id=gif_id, **kwargs)
        return self._new_object(obj)

    def new_sticker(self, sticker_id: str, **kwargs):
        """Creates a new sticker with specified parameters and appends it to the list."""
        obj = InlineQueryResultCachedSticker(id=str(self._counter), sticker_file_id=sticker_id, **kwargs)
        return self._new_object(obj)

    def new_audio(self, audio_id: str, **kwargs) -> "InlineQueryResultsBuilder":
        """Creates a new audio with specified parameters and appends it to the list."""
        obj = InlineQueryResultCachedAudio(id=str(self._counter), audio_file_id=audio_id, **kwargs)
        return self._new_object(obj)

    def new_voice(self, voice_id: str, title: str, **kwargs) -> "InlineQueryResultsBuilder":
        """Creates a new voice with specified parameters and appends it to the list."""
        obj = InlineQueryResultCachedVoice(id=str(self._counter), voice_file_id=voice_id, title=title, **kwargs)
        return self._new_object(obj)

    def new_document(self, title: str, file_id: str, **kwargs):
        """Creates a new document with specified parameters and appends it to the list."""
        obj = InlineQueryResultCachedDocument(id=str(self._counter), title=title, document_file_id=file_id, **kwargs)
        return self._new_object(obj)
