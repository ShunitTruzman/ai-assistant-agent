"""
Tests for the pure routing logic. These need no API keys, no browser, and no LLM —
they verify the graph's decision-making directly.

Run with: pytest
"""
from logic import worker_route, evaluation_route


def test_worker_route_to_tools_when_tool_calls():
    assert worker_route(True) == "tools"


def test_worker_route_to_evaluator_when_no_tool_calls():
    assert worker_route(False) == "evaluator"


def test_evaluation_ends_when_criteria_met():
    assert evaluation_route(True, False, iterations=1, max_iterations=3) == "END"


def test_evaluation_ends_when_user_input_needed():
    assert evaluation_route(False, True, iterations=1, max_iterations=3) == "END"


def test_evaluation_retries_when_not_met_and_under_cap():
    assert evaluation_route(False, False, iterations=1, max_iterations=3) == "worker"


def test_evaluation_stops_at_iteration_cap():
    # The safety net: even if not met, stop once the cap is reached.
    assert evaluation_route(False, False, iterations=3, max_iterations=3) == "END"
