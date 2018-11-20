import pytest
from hypothesis import given
from hypothesis.strategies import integers, text, characters

import util


@given(integers())
def test_parse_int_with_numbers(x):
    assert util.try_parse_int(str(x)) == x


@given(text(alphabet=characters(blacklist_categories='Cc,N')))
def test_parse_int_with_strings(x):
    assert util.try_parse_int(x) is None


@pytest.mark.parametrize("s,expected", [
    ("1 2 3 4 5", [1, 2, 3, 4, 5]),
    ("-6 20 0 47 -12", [-6, 20, 0, 47, -12]),
    ("0.5 -1.25 41.9", None),
    ("foo bar", None),
    ("baz", None),
    ("", None),
])
def test_extract_numbers(s, expected):
    assert util.try_extract_numbers(s) == expected
