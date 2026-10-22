import os

from src.cli import main, restore_shell_symbols


def test_prints_steps_and_result(capsys):
    assert main(["2", "3", "+"]) == 0
    out = capsys.readouterr().out
    assert "3  ->  [2, 3]" in out
    assert "2 3 + = 5" in out


def test_expression_in_quotes_also_works(capsys):
    assert main(["2 3 +"]) == 0
    assert "2 3 + = 5" in capsys.readouterr().out


def test_tilde_replaced_by_shell_with_home(capsys):
    # bash без кавычек превращает ~ в домашнюю папку
    home = os.path.expanduser("~")
    assert main(["2", "3", home]) == 0
    assert "2 3 ~ = 1" in capsys.readouterr().out


def test_star_replaced_by_shell_with_files(tmp_path, monkeypatch):
    # bash без кавычек превращает * в список файлов текущей папки
    monkeypatch.chdir(tmp_path)
    (tmp_path / "a.txt").touch()
    (tmp_path / "b.txt").touch()
    assert restore_shell_symbols(["2", "3", "a.txt", "b.txt"]) == ["2", "3", "*"]


def test_no_args_shows_usage(capsys):
    assert main([]) == 1
    assert "Использование" in capsys.readouterr().out


def test_help(capsys):
    assert main(["--help"]) == 0
    assert "Использование" in capsys.readouterr().out


def test_error_is_explained(capsys):
    assert main(["5", "0", "/"]) == 1
    assert "деление на ноль" in capsys.readouterr().err
