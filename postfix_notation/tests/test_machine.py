import pytest

from src.machine import StackMachineError, evaluate


def result_of(expression):
    result, _ = evaluate(expression)
    return result


@pytest.mark.parametrize(
    "expression, expected",
    [
        ("3 0 4 ~ 2 ~", 47),
        ("2 2 + 4 - 4 ~ 2 3 * +", 22),
    ],
)
def test_examples_from_task(expression, expected):
    assert result_of(expression) == expected


@pytest.mark.parametrize(
    "expression, expected",
    [
        ("2 3 +", 5),
        ("2 3 -", -1),
        ("2 3 *", 6),
        ("6 3 /", 2),
        ("7 2 /", 3.5),
        ("-1.5 4 +", 2.5),
    ],
)
def test_operators(expression, expected):
    assert result_of(expression) == expected


def test_tilde_without_zero_gives_abs_difference():
    assert result_of("2 7 ~") == 5


def test_tilde_with_zero_squares_sum_of_stack():
    # (1 + 2 + 0 + 4) ** 2 = 49
    assert result_of("1 2 0 4 ~") == 49


def test_steps():
    _, steps = evaluate("3 0 4 ~")
    assert steps == [("3", [3]), ("0", [3, 0]), ("4", [3, 0, 4]), ("~", [49])]


@pytest.mark.parametrize(
    "expression, message",
    [
        ("", "пустое"),
        ("2 abc +", "не понимаю"),
        ("2 +", "нужно два числа"),
        ("5 0 /", "деление на ноль"),
        ("1 2 3 +", "не хватает операции"),
    ],
)
def test_errors(expression, message):
    with pytest.raises(StackMachineError, match=message):
        evaluate(expression)
