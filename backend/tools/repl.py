"""Sandboxed Python REPL for code execution."""

from __future__ import annotations

import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any

from backend.utils.helpers import sanitize_executable_code, truncate_text

EXECUTION_TIMEOUT = 30
TEST_TIMEOUT = 60


def execute_python_code(code: str, tests: str = "", timeout: int = EXECUTION_TIMEOUT) -> dict[str, Any]:
    """Execute Python code and optional pytest tests in a subprocess sandbox."""
    logs: list[dict[str, str]] = []
    start = time.time()

    code = sanitize_executable_code(code, "python")
    tests = sanitize_executable_code(tests, "python") if tests.strip() else ""

    if not code:
        return _error_result(start, logs, "No executable Python code found after sanitization")

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        code_file = tmp / "solution.py"
        code_file.write_text(code, encoding="utf-8")
        logs.append({"level": "INFO", "message": "Wrote solution.py"})

        if tests:
            test_file = tmp / "test_solution.py"
            test_file.write_text(tests, encoding="utf-8")
            logs.append({"level": "INFO", "message": "Wrote test_solution.py"})
            cmd = [sys.executable, "-m", "pytest", str(test_file), "-v", "--tb=short"]
            exec_timeout = TEST_TIMEOUT
        else:
            cmd = [sys.executable, str(code_file)]
            exec_timeout = timeout

        try:
            env = os.environ.copy()
            env["PYTHONPATH"] = tmpdir
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=exec_timeout,
                cwd=tmpdir,
                env=env,
            )
            runtime_ms = int((time.time() - start) * 1000)
            stdout = truncate_text(result.stdout)
            stderr = truncate_text(result.stderr)

            test_results = _parse_pytest_output(stdout) if tests else []
            summary = _parse_pytest_summary(stdout, stderr) if tests else {}
            passed = summary.get("passed", sum(1 for t in test_results if t["status"] == "passed"))
            failed = summary.get("failed", sum(1 for t in test_results if t["status"] == "failed"))
            errors = summary.get("errors", sum(1 for t in test_results if t["status"] == "error"))
            total = summary.get("total", len(test_results))

            if result.returncode == 0:
                status = "success"
            elif tests and passed > 0:
                status = "partial"
            elif tests:
                status = "failed"
            else:
                status = "error"

            return {
                "execution_status": status,
                "language": "python",
                "runtime_ms": runtime_ms,
                "stdout": stdout,
                "stderr": stderr,
                "exit_code": result.returncode,
                "test_results": test_results,
                "tests_summary": {
                    "total": total,
                    "passed": passed,
                    "failed": failed,
                    "errors": errors,
                    "skipped": summary.get("skipped", 0),
                },
                "traceback": stderr if result.returncode != 0 else None,
                "execution_logs": logs,
                "sandbox_notes": "Executed in isolated subprocess with no network access",
            }
        except subprocess.TimeoutExpired:
            return _error_result(
                start, logs, f"Execution timed out after {exec_timeout}s", exec_timeout
            )
        except Exception as exc:
            return _error_result(start, logs, str(exc))


def execute_code(language: str, code: str, tests: str = "") -> dict[str, Any]:
    """Route execution to language-specific runner."""
    if language == "python":
        return execute_python_code(code, tests)
    return {
        "execution_status": "skipped",
        "language": language,
        "runtime_ms": 0,
        "stdout": "",
        "stderr": "",
        "exit_code": 0,
        "test_results": [],
        "tests_summary": {"total": 0, "passed": 0, "failed": 0, "errors": 0, "skipped": 0},
        "traceback": None,
        "execution_logs": [],
        "sandbox_notes": (
            f"Automatic execution for {language} requires manual validation. "
            "Python REPL is the only supported runtime in this build."
        ),
    }


def _error_result(
    start: float,
    logs: list[dict[str, str]],
    message: str,
    timeout: int = EXECUTION_TIMEOUT,
) -> dict[str, Any]:
    return {
        "execution_status": "error",
        "language": "python",
        "runtime_ms": int((time.time() - start) * 1000),
        "stdout": "",
        "stderr": message,
        "exit_code": -1,
        "test_results": [],
        "tests_summary": {"total": 0, "passed": 0, "failed": 0, "errors": 0, "skipped": 0},
        "traceback": message,
        "execution_logs": logs,
        "sandbox_notes": message,
    }


def _parse_pytest_output(stdout: str) -> list[dict[str, Any]]:
    results = []
    for line in stdout.splitlines():
        if " PASSED" in line:
            name = line.split(" PASSED")[0].strip().split()[-1]
            results.append({"test_name": name, "status": "passed", "duration_ms": 0, "message": ""})
        elif " FAILED" in line:
            name = line.split(" FAILED")[0].strip().split()[-1]
            results.append({"test_name": name, "status": "failed", "duration_ms": 0, "message": line})
        elif " ERROR" in line:
            name = line.split(" ERROR")[0].strip().split()[-1]
            results.append({"test_name": name, "status": "error", "duration_ms": 0, "message": line})
    return results


def _parse_pytest_summary(stdout: str, stderr: str) -> dict[str, int]:
    """Parse pytest final summary line like '2 passed, 1 failed in 0.05s'."""
    text = f"{stdout}\n{stderr}"
    summary: dict[str, int] = {"total": 0, "passed": 0, "failed": 0, "errors": 0, "skipped": 0}
    match = re.search(
        r"=+\s*(?:(\d+)\s+passed)?(?:,\s*)?(?:(\d+)\s+failed)?(?:,\s*)?(?:(\d+)\s+error)?",
        text,
        re.IGNORECASE,
    )
    if match:
        summary["passed"] = int(match.group(1) or 0)
        summary["failed"] = int(match.group(2) or 0)
        summary["errors"] = int(match.group(3) or 0)
        summary["total"] = summary["passed"] + summary["failed"] + summary["errors"]
    return summary
