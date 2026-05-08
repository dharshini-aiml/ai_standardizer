"""LangGraph workflow for data standardization."""

from langgraph.graph import StateGraph, END


def validate_node(state: dict) -> dict:
    """Validation step."""
    data = state.get("data", {})
    errors = []

    if not data.get("document_id"):
        errors.append("Missing document_id")

    if not data.get("extracted_fields"):
        errors.append("Missing extracted_fields")

    state["validation_errors"] = errors
    return state


def format_node(state: dict) -> dict:
    """Formatting step."""
    data = state.get("data", {})
    extracted = data.get("extracted_fields", {})

    formatted = {}

    for key, value in extracted.items():
        clean_key = key.strip().lower()

        if isinstance(value, str):
            value = value.strip()

        formatted[clean_key] = value

    state["formatted_data"] = formatted
    return state


def fix_node(state: dict) -> dict:
    """Cleaning and standardization step."""
    formatted = state.get("formatted_data", {})
    standardized = {}

    for key, value in formatted.items():

        if "email" in key and isinstance(value, str):
            standardized[key] = value.lower()

        elif "phone" in key and isinstance(value, str):
            digits = "".join(filter(str.isdigit, value))
            standardized[key] = digits

        elif "name" in key and isinstance(value, str):
            standardized[key] = " ".join(value.split()).title()

        else:
            standardized[key] = value

    state["standardized_data"] = standardized
    state["quality_score"] = 0.95
    state["document_type"] = state.get("data", {}).get("source", "unknown")

    return state


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