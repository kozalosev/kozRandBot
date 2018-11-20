import pytest
from hypothesis import given
from hypothesis.strategies import integers

from handler import impls


def test_matching_flip_coin():
    assert impls.FlipCoinHandler.can_process("")
    assert not impls.FlipCoinHandler.can_process("foo")


class TestMatchingRandNum:
    @staticmethod
    @pytest.mark.parametrize("s", ["", "foo", "foo bar", "100 bar"])
    def test_non_numerical_strings(s):
        assert not impls.RandNumHandler.can_process(s)

    @staticmethod
    @given(integers())
    def test_one_number(x):
        assert impls.RandNumHandler.can_process(str(x))

    @staticmethod
    @given(integers(), integers())
    def test_pair_numbers(a, b):
        assert impls.RandNumHandler.can_process(f"{a} {b}")
        assert impls.RandNumHandler.can_process(f"{a}, {b}")
        assert impls.RandNumHandler.can_process(f"{a}; {b}")


def test_matching_yes_no():
    assert impls.YesNoHandler.can_process("Is it working?")
    assert not impls.YesNoHandler.can_process("foo bar")


class TestMatchingRandItem:
    @staticmethod
    @pytest.mark.parametrize("s", ["one, two, three", "Beer, wine or vodka?", "one, two; three, four", "1, 2, 3"])
    def test_success(s):
        assert impls.RandItemHandler.can_process(s)

    @staticmethod
    def test_fail():
        assert not impls.RandItemHandler.can_process("foo bar")


class TestMatchingPassword:
    @staticmethod
    def test_empty_str():
        assert impls.PasswordHandler.can_process("")

    @staticmethod
    @pytest.mark.parametrize("s", ["foo", "foo bar", "100 bar"])
    def test_non_numerical_strings(s):
        assert not impls.PasswordHandler.can_process(s)

    @staticmethod
    @given(integers(min_value=6, max_value=2048))
    def test_one_number_in_range(x):
        assert impls.PasswordHandler.can_process(str(x))

    @staticmethod
    @given(integers(min_value=-5, max_value=5))
    def test_too_small_numbers(x):
        assert not impls.PasswordHandler.can_process(str(x))

    @staticmethod
    @given(integers(min_value=2049))
    def test_too_bit_positive_numbers(x):
        assert not impls.PasswordHandler.can_process(str(x))

    @staticmethod
    @given(integers(max_value=-2049))
    def test_too_bit_negative_numbers(x):
        assert not impls.PasswordHandler.can_process(str(x))
