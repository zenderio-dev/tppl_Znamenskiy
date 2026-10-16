import pytest

from src.machine import StackMachine, StackMachineError, evaluate, normalize, parse_number


class TestExamples:
    def test_first_example(self):
        assert evaluate("3 0 4 ~ 2 ~") == 47

    def test_second_example(self):
        assert evaluate("2 2 + 4 - 4 ~ 2 3 * +") == 22


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


class TestTilde:
    def test_both_not_zero_gives_abs_difference(self):
        assert evaluate("2 7 ~") == 5
        assert evaluate("7 2 ~") == 5

    def test_keeps_rest_of_stack_when_not_zero(self):
        machine = StackMachine()
        for token in "1 2 7 ~".split():
            machine.step(token)
        assert machine.stack == [1, 5]

    @pytest.mark.parametrize("expression", ["1 2 0 4 ~", "1 2 4 0 ~"])
    def test_zero_operand_squares_sum_of_stack(self, expression):
        # (1 + 2 + 0 + 4) ** 2 = 49
        assert evaluate(expression) == 49

    def test_zero_operand_replaces_whole_stack(self):
        machine = StackMachine()
        for token in "1 2 0 4 ~".split():
            machine.step(token)
        assert machine.stack == [49]

    def test_both_zero(self):
        assert evaluate("0 0 ~") == 0


class TestSteps:
    def test_on_step_gets_stack_after_each_token(self):
        steps = []
        evaluate("3 0 4 ~ 2 ~", on_step=lambda token, stack: steps.append((token, stack)))
        assert steps == [
            ("3", [3]),
            ("0", [3, 0]),
            ("4", [3, 0, 4]),
            ("~", [49]),
            ("2", [49, 2]),
            ("~", [47]),
        ]


class TestErrors:
    def test_empty_expression(self):
        with pytest.raises(StackMachineError, match="пустое"):
            evaluate("   ")

    def test_unknown_token(self):
        with pytest.raises(StackMachineError, match="не понимаю 'abc'"):
            evaluate("2 abc +")

    @pytest.mark.parametrize("expression", ["+", "2 +", "5 ~"])
    def test_not_enough_operands(self, expression):
        with pytest.raises(StackMachineError, match="нужно два числа"):
            evaluate(expression)

    def test_division_by_zero(self):
        with pytest.raises(StackMachineError, match="деление на ноль"):
            evaluate("5 0 /")

    def test_too_many_values_left(self):
        with pytest.raises(StackMachineError, match="не хватает операции"):
            evaluate("1 2 3 +")


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
