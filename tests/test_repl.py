"""Tests for Python REPL execution."""

from backend.tools.repl import execute_python_code, execute_code


def test_execute_simple_python():
    code = 'print("hello")'
    result = execute_python_code(code)
    assert result["execution_status"] == "success"
    assert "hello" in result["stdout"]


def test_execute_python_with_syntax_error():
    code = "def broken(\n    pass"
    result = execute_python_code(code)
    assert result["execution_status"] == "error"


def test_execute_python_with_tests():
    code = "def add(a, b):\n    return a + b"
    tests = (
        "from solution import add\n\n"
        "def test_add():\n"
        "    assert add(1, 2) == 3\n"
    )
    result = execute_python_code(code, tests)
    assert result["execution_status"] in ("success", "partial", "failed")


def test_execute_non_python_skipped():
    result = execute_code("java", "public class Main {}")
    assert result["execution_status"] == "skipped"
