"""Tests for code sanitization before execution."""

from backend.tools.repl import execute_python_code
from backend.utils.helpers import sanitize_executable_code


def test_sanitize_strips_markdown_fences():
    raw = "```python\ndef hello():\n    return 1\n```"
    assert "def hello" in sanitize_executable_code(raw)
    assert "```" not in sanitize_executable_code(raw)


def test_execute_fenced_code_succeeds():
    code = "```python\ndef greet():\n    print('hi')\n\nif __name__ == '__main__':\n    greet()\n```"
    result = execute_python_code(code)
    assert result["execution_status"] == "success"
    assert "hi" in result["stdout"]
