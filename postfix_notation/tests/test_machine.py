import pytest

from src.machine import StackMachineError, evaluate, normalize, parse_number


class TestOperators:
    @pytest.mark.parametrize(
        "expression, expected",
        [
            ("2 3 +", 5),
            ("2 3 -", -1),
            ("2 3 *", 6),
            ("6 3 /", 2),
            ("7 2 /", 3.5),
            ("1.5 1.5 +", 3),
            ("-2 5 *", -10),
            ("42", 42),
        ],
    )
    def test_operator(self, expression, expected):
        assert evaluate(expression) == expected

    def test_division_result_is_int_when_whole(self):
        assert isinstance(evaluate("6 3 /"), int)

    def test_extra_spaces_are_ignored(self):
        assert evaluate("  2   3  + ") == 5

    def test_division_by_zero(self):
        with pytest.raises(StackMachineError, match="деление на ноль"):
            evaluate("5 0 /")


class TestHelpers:
    def test_parse_int(self):
        assert parse_number("12") == 12
        assert isinstance(parse_number("12"), int)

    def test_parse_float(self):
        assert parse_number("2.5") == 2.5

    def test_normalize(self):
        assert normalize(4.0) == 4
        assert isinstance(normalize(4.0), int)
        assert normalize(2.5) == 2.5
        assert normalize(7) == 7
