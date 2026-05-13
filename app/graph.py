"""LangGraph workflow for data standardization."""

from langgraph.graph import StateGraph, END
from app.agents.type_detector import TypeDetector
from app.agents.validator import validate_json as validate_state
from app.agents.formatter import format_json as format_state
from app.agents.fixer import fix_json as fix_state


def validate_node(state: dict) -> dict:
    """Validation step."""
    return validate_state(state)


def format_node(state: dict) -> dict:
    """Formatting step."""
    if not state.get("is_valid", False):
        return state

    return format_state(state)


def fix_node(state: dict) -> dict:
    """Cleaning and standardization step."""
    if not state.get("is_valid", False):
        return state

    updated_state = fix_state(state)
    updated_state["document_type"] = TypeDetector.detect_document_type(
        updated_state.get("standardized_data", {})
    )
    return updated_state


def build_graph():
    """Build LangGraph workflow."""
    workflow = StateGraph(dict)

    workflow.add_node("validate", validate_node)
    workflow.add_node("format", format_node)
    workflow.add_node("fix", fix_node)

    workflow.set_entry_point("validate")

    workflow.add_edge("validate", "format")
    workflow.add_edge("format", "fix")
    workflow.add_edge("fix", END)

    return workflow.compile()