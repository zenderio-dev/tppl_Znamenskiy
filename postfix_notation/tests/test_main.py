from src.main import main


def test_prints_steps_and_result(capsys):
    assert main(["2 3 +"]) == 0
    out = capsys.readouterr().out
    assert "3  ->  [2, 3]" in out
    assert "2 3 + = 5" in out


def test_no_args_shows_usage(capsys):
    assert main([]) == 1
    assert "Использование" in capsys.readouterr().out


def test_help(capsys):
    assert main(["--help"]) == 0
    assert "Использование" in capsys.readouterr().out


def test_error_is_explained(capsys):
    assert main(["5 0 /"]) == 1
    assert "деление на ноль" in capsys.readouterr().err
