"""Deterministic evaluation from execution results — drives the regeneration loop."""

from __future__ import annotations

from backend.models.state import CodeForgeState

MAX_REGENERATION_LOOPS = 2


def evaluate_execution(state: CodeForgeState) -> dict:
    """Build evaluation dict from execution results. No LLM call — reliable loop control."""
    exec_result = state.get("execution_result") or {}
    status = exec_result.get("execution_status", "skipped")
    summary = exec_result.get("tests_summary") or {}
    total = int(summary.get("total", 0))
    passed = int(summary.get("passed", 0))
    failed = int(summary.get("failed", 0))
    errors = int(summary.get("errors", 0))
    loop_count = state.get("loop_count", 0)

    if total > 0:
        test_pass_rate = round(passed / total, 2)
    elif status == "success":
        test_pass_rate = 1.0
    else:
        test_pass_rate = 0.0

    failed_tests = [
        tr for tr in exec_result.get("test_results", [])
        if tr.get("status") in ("failed", "error")
    ]

    suggestions = []
    if exec_result.get("stderr"):
        suggestions.append({
            "priority": "high",
            "area": "correctness",
            "suggestion": f"Fix runtime error: {str(exec_result['stderr'])[:300]}",
        })
    for tr in failed_tests[:5]:
        suggestions.append({
            "priority": "high",
            "area": "tests",
            "suggestion": f"Fix failing test '{tr.get('test_name')}': {tr.get('message', '')[:200]}",
        })

    needs_fix = (
        status in ("failed", "partial", "error")
        or failed > 0
        or errors > 0
        or (total > 0 and passed < total)
    )

    can_retry = loop_count < MAX_REGENERATION_LOOPS
    should_regenerate = needs_fix and can_retry

    regenerate_agent = "language_specialist"
    if needs_fix and state.get("security_report", {}).get("verdict") == "FAIL":
        regenerate_agent = "language_specialist"
    elif needs_fix and failed == 0 and status == "error":
        regenerate_agent = "optimization"

    if needs_fix and not can_retry:
        verdict = "FAIL"
        summary_text = (
            f"Execution {status} after {loop_count} fix attempt(s): "
            f"{passed}/{total} tests passed. Max retries reached."
        )
    elif needs_fix:
        verdict = "FAIL"
        summary_text = (
            f"Execution {status}: {passed}/{total} tests passed. "
            f"Regenerating code (attempt {loop_count + 1}/{MAX_REGENERATION_LOOPS})."
        )
    else:
        verdict = "PASS"
        summary_text = f"Execution {status}: {passed}/{total} tests passed."

    return {
        "verdict": verdict,
        "confidence_score": test_pass_rate,
        "test_pass_rate": test_pass_rate,
        "scores": {
            "correctness": int(test_pass_rate * 100),
            "test_coverage": int(test_pass_rate * 100),
        },
        "requirements_met": [] if needs_fix else ["Code executes successfully"],
        "requirements_missing": [] if not needs_fix else ["Fix failing tests or runtime errors"],
        "improvement_suggestions": suggestions,
        "evaluation_summary": summary_text,
        "should_regenerate": should_regenerate,
        "regenerate_agent": regenerate_agent if should_regenerate else None,
        "failed_tests": failed_tests,
    }
