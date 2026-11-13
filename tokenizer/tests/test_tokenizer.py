import pytest

from lexer import Lexer
from lexer.token import TokenType
from main import main


def test_words_and_positions():
    tokens = Lexer("if else while return for def # @\n\t_if9 if_else").tokenize()
    assert [(t.type_, t.value) for t in tokens] == [
        (TokenType.KEYWORD, word) for word in "if else while return for def".split()
    ] + [(TokenType.IDENT, "_if9"), (TokenType.IDENT, "if_else")]
    assert [(t.line, t.column) for t in tokens[-2:]] == [(2, 2), (2, 7)]


@pytest.mark.parametrize(
    "source, kind",
    [
        ("42", "INT"),
        ("3.14", "FLOAT"),
        (".5", "FLOAT"),
        ("1.", "FLOAT"),
        ('"hello # world"', "STRING"),
        ('""', "STRING"),
    ],
)
def test_literals(source, kind):
    assert [str(t) for t in Lexer(source).tokenize()] == [f"({kind}, {source}, 1:1)"]


def test_operators_and_separators():
    operators = "+ - * / = < > == <= >="
    separators = "(){} ,;"
    tokens = Lexer(f"{operators} {separators} # comment").tokenize()
    assert [(t.type_, t.value) for t in tokens] == [
        (TokenType.OP, char) for char in operators.split()
    ] + [(TokenType.SEP, char) for char in separators if char != " "]


def test_file_output(tmp_path, capsys):
    path = tmp_path / "input.txt"
    path.write_text("x = y * 2 + z * 3", encoding="utf-8")
    assert main([str(path)]) == 0
    output = capsys.readouterr()
    assert output.out.splitlines() == [
        "(IDENT, x, 1:1)", "(OP, =, 1:3)", "(IDENT, y, 1:5)",
        "(OP, *, 1:7)", "(INT, 2, 1:9)", "(OP, +, 1:11)",
        "(IDENT, z, 1:13)", "(OP, *, 1:15)", "(INT, 3, 1:17)",
    ]
    assert output.err == ""


@pytest.mark.parametrize(
    "source, error",
    [
        ("a @ b", "1:3: lexical: unexpected character '@'"),
        ('a\n  "open', "2:3: lexical: unterminated string literal"),
        ('"open\n"', "1:1: lexical: unterminated string literal"),
        (".", "1:1: lexical: unexpected character '.'"),
    ],
)
def test_lexical_errors(source, error, tmp_path, capsys):
    path = tmp_path / "input.txt"
    path.write_text(source, encoding="utf-8")
    assert main([str(path)]) != 0
    output = capsys.readouterr()
    assert output.out == ""
    assert output.err == f"{path}:{error}\n"


def test_missing_file(tmp_path, capsys):
    path = tmp_path / "missing.txt"
    assert main([str(path)]) != 0
    assert capsys.readouterr().err.startswith(f"{path}:1:1: lexical: ")


def test_missing_argument(capsys):
    assert main([]) != 0
    assert "Usage:" in capsys.readouterr().err
