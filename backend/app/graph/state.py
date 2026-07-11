"""
LangGraph agent state definition.

This TypedDict defines the shape of data flowing through every
node in the agent graph. The `messages` field uses LangGraph's
`add_messages` reducer for automatic message list management.

WHY TypedDict over Pydantic?
  - LangGraph's StateGraph requires TypedDict for state definitions
  - add_messages annotation enables LangGraph's native message
    deduplication and append semantics
"""

from __future__ import annotations

from typing import Annotated, Any, Optional

from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage


class AgentState(dict):
    """State schema for the IntelliHCP LangGraph agent.

    Fields:
        messages: Conversation history managed by LangGraph's add_messages reducer.
                  New messages are appended; duplicates are deduplicated by ID.

        current_form: Current interaction form state from the frontend.
                      Used by the llm_node to build dynamic system prompt context
                      so the LLM knows which interaction to reference for edits.
                      Overwritten (last-write-wins) each invocation — not accumulated.
    """
    messages: Annotated[list[BaseMessage], add_messages]
    current_form: dict[str, Any]


# We use a proper TypedDict annotation for LangGraph
from typing import TypedDict


class AgentState(TypedDict):
    """State schema for the IntelliHCP LangGraph agent."""
    messages: Annotated[list[BaseMessage], add_messages]
    current_form: dict[str, Any]
