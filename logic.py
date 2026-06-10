"""
Pure routing logic for the agent graph.

These functions contain the graph's decision-making with no heavy dependencies, so they
can be unit-tested without importing LangGraph, Playwright, or hitting any API. The graph
nodes in `assistant.py` delegate their routing decisions here.
"""

from __future__ import annotations


def worker_route(has_tool_calls: bool) -> str:
    """After the worker speaks: run tools if it asked for them, otherwise evaluate."""
    return "tools" if has_tool_calls else "evaluator"


def evaluation_route(success_criteria_met: bool, user_input_needed: bool,
                     iterations: int, max_iterations: int) -> str:
    """
    After the evaluator judges the worker's answer, decide where to go next.

    End the run when the criteria are met, when the user needs to weigh in, OR when we've
    hit the iteration cap (this last guard is the safety net the original lacked — without
    it the worker/evaluator loop can spin forever if the evaluator keeps rejecting).
    Otherwise, send it back to the worker for another attempt.
    """
    if success_criteria_met or user_input_needed:
        return "END"
    if iterations >= max_iterations:
        return "END"
    return "worker"
