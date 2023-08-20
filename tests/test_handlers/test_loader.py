import pytest
from klocmod import LanguageDictionary

from handler.abc import InlineHandler, Universal
from handler.loader import InlineHandlersLoader
from handler import impls


def test_load_impls():
    loader = InlineHandlersLoader()
    expected_set = {impls.FlipCoinHandler, impls.RandNumHandler, impls.YesNoHandler, impls.RandItemHandler,
                    impls.PasswordHandler, impls.HEXPasswordHandler, impls.UUIDHandler}
    assert expected_set == loader.handlers


@pytest.mark.parametrize("query,expected_type_set", [
    ("", {impls.FlipCoinHandler, impls.PasswordHandler}),
    ("50", {impls.RandNumHandler, impls.PasswordHandler}),
    ("50 100", {impls.RandNumHandler}),
    ("50 -100", {impls.RandNumHandler}),
    ("Is it working?", {impls.YesNoHandler}),
    ("programming or dating with girls", {impls.RandItemHandler}),
    ("Beer, wine or vodka?", {impls.YesNoHandler, impls.RandItemHandler}),
])
def test_matching_impls(query, expected_type_set):
    loader = InlineHandlersLoader()
    types = {type(handler) for handler in loader.match_handlers(query)}
    assert expected_type_set == types


def test_name_property():
    class FooBar(Universal, InlineHandler):
        def get_text(self, query: str, lang: LanguageDictionary) -> str:
            return ""

    class FooBarInline(FooBar):
        pass

    class FooBarInlineHandler(FooBar):
        pass

    for handler in [FooBar, FooBarInline, FooBarInlineHandler]:
        assert "foo_bar" == handler.name == handler().name
