import runpy
import sys

import pytest

from src.main import format_stack, main


def test_prints_steps_and_result(capsys):
    assert main(["3 0 4 ~ 2 ~"]) == 0
    out = capsys.readouterr().out
    assert "Вычисляю: 3 0 4 ~ 2 ~" in out
    assert "->  [3, 0, 4]" in out
    assert "->  [49]" in out
    assert out.strip().endswith("3 0 4 ~ 2 ~ = 47")


def test_expression_split_into_several_args(capsys):
    assert main(["2", "3", "+"]) == 0
    assert "2 3 + = 5" in capsys.readouterr().out


def test_no_args_shows_usage(capsys):
    assert main([]) == 1
    out = capsys.readouterr().out
    assert "Вы не передали выражение" in out
    assert "Использование" in out


@pytest.mark.parametrize("flag", ["-h", "--help"])
def test_help(capsys, flag):
    assert main([flag]) == 0
    assert "Использование" in capsys.readouterr().out


def test_error_is_explained(capsys):
    assert main(["5 0 /"]) == 1
    captured = capsys.readouterr()
    assert "Не получилось вычислить: деление на ноль" in captured.err
    assert "Подсказка" in captured.err
    assert "->  [5, 0]" in captured.out


def test_format_stack():
    assert format_stack([]) == "[]"
    assert format_stack([1, 2.5]) == "[1, 2.5]"


def test_run_as_module(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["main", "2 3 *"])
    monkeypatch.delitem(sys.modules, "src.main", raising=False)
    with pytest.raises(SystemExit) as exit_info:
        runpy.run_module("src.main", run_name="__main__")
    assert exit_info.value.code == 0
    assert "2 3 * = 6" in capsys.readouterr().out
