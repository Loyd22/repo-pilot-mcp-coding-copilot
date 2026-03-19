"""
LangGraph workflow definition for the repository assistant.
"""

from langgraph.graph import END, START, StateGraph

from app.agent.nodes import (
    classify_request_node,
    generate_answer_node,
    load_memory_node,
    run_tool_node,
)
from app.agent.state import RepoAgentState


def build_repo_agent():
    """Build and compile the repository assistant workflow graph."""
    graph = StateGraph(RepoAgentState)

    graph.add_node("load_memory", load_memory_node)
    graph.add_node("classify_request", classify_request_node)
    graph.add_node("run_tool", run_tool_node)
    graph.add_node("generate_answer", generate_answer_node)

    graph.add_edge(START, "load_memory")
    graph.add_edge("load_memory", "classify_request")
    graph.add_edge("classify_request", "run_tool")
    graph.add_edge("run_tool", "generate_answer")
    graph.add_edge("generate_answer", END)

    return graph.compile()