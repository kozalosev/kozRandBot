import pytest
from hypothesis import given, assume
from hypothesis.strategies import integers

import rand


@pytest.mark.parametrize("a,b", [
    ("foo", "bar"),
    (1, 2),
    (5.0, -30),
    (object(), bool),
])
def test_one_out_of_two(a, b):
    values = [rand.one_out_of_two(a, b) for _ in range(100)]
    assert all(v in [a, b] for v in values)
    assert not all(v == a for v in values)
    assert not all(v == b for v in values)


@given(integers(), integers())
def test_between(n, m):
    assume(n <= m)
    assert n <= rand.between(n, m) <= m


@given(integers(), integers())
def test_between_reversed_args(n, m):
    assume(n > m)
    assert n >= rand.between(n, m) >= m


@given(integers())
def test_maximum_with_positive_value(m):
    assume(m > 0)
    assert 1 <= rand.maximum(m) <= m


@given(integers())
def test_maximum_with_negative_values(m):
    assume(m < 0)
    assert -1 >= rand.maximum(m) >= m


def test_maximum_with_zero():
    assert 0 <= rand.maximum(0) < 1


@pytest.mark.parametrize("length", [-100, 20, 50, 0])
def test_password(length):
    assert len(rand.password(length)) == abs(length)


def test_is_password_strong():
    extra_chars = "#$%+!"
    assert rand._is_password_strong("abC2D1%", extra_chars)
    assert not rand._is_password_strong("abC2D1", extra_chars)
    assert rand._is_password_strong("abC2D1", "")
    assert not rand._is_password_strong("abCD%", extra_chars)
    assert not rand._is_password_strong("ABC2D1%", extra_chars)
    assert not rand._is_password_strong("abc2d1%", extra_chars)
