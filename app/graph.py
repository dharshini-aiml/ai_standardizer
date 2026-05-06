"""LangGraph workflow for data standardization pipeline."""
from typing import Dict, Any, TypedDict
from langgraph.graph import StateGraph, END
from app.agents.validator import validate_json
from app.agents.formatter import format_json
from app.agents.fixer import fix_json
from app.utils.logger import logger


class PipelineState(TypedDict, total=False):
    """State schema for the standardization pipeline."""
    
    # Input data
    data: Dict[str, Any]
    
    # Validation results
    is_valid: bool
    validation_errors: list[str]
    
    # Formatting results
    formatted_data: Dict[str, Any]
    formatting_error: str
    
    # Final standardized results
    standardized_data: Dict[str, Any]
    quality_score: float
    fixing_error: str


def should_continue_to_format(state: PipelineState) -> str:
    """
    Conditional router: continue to format only if validation passed.
    
    Args:
        state: Current pipeline state
        
    Returns:
        Next node name
    """
    if state.get("is_valid", False):
        logger.debug("Validation passed, proceeding to formatting")
        return "format"
    else:
        logger.error("Validation failed, terminating pipeline")
        return END


def should_continue_to_fix(state: PipelineState) -> str:
    """
    Conditional router: continue to fix only if formatting succeeded.
    
    Args:
        state: Current pipeline state
        
    Returns:
        Next node name
    """
    # The StateGraph may pre-populate optional keys (e.g. with None),
    # so check the value rather than just the presence of the key.
    if not state.get("formatting_error"):
        logger.debug("Formatting completed, proceeding to fixing")
        return "fix"
    else:
        logger.error("Formatting failed, terminating pipeline")
        return END


def build_graph() -> Any:
    """
    Build the LangGraph workflow for data standardization.
    
    Returns:
        Compiled graph ready for execution
    """
    # Create the state graph
    graph = StateGraph(PipelineState)
    
    # Add nodes for each processing step
    graph.add_node("validate", validate_json)
    graph.add_node("format", format_json)
    graph.add_node("fix", fix_json)
    
    # Set entry point
    graph.set_entry_point("validate")
    
    # Add conditional edges based on validation
    graph.add_conditional_edges(
        "validate",
        should_continue_to_format,
        {
            "format": "format",
            END: END
        }
    )
    
    # Add conditional edges based on formatting
    graph.add_conditional_edges(
        "format",
        should_continue_to_fix,
        {
            "fix": "fix",
            END: END
        }
    )
    
    # Finalize pipeline
    graph.add_edge("fix", END)
    
    # Compile and return
    compiled_graph = graph.compile()
    logger.info("Standardization pipeline graph built successfully")
    
    return compiled_graph
