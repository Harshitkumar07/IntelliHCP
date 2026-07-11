"""
Chat endpoint request / response schemas.

ChatRequest carries the user message, session identifier, and the
current form state (so the agent has context for edits).
ChatResponse carries the AI reply, which tool was used, and the
form_data payload that Redux merges into the interaction slice.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Inbound chat message from the frontend."""

    message: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="User's natural language message",
    )
    session_id: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Conversation thread identifier for MemorySaver",
    )
    current_form: dict | None = Field(
        default=None,
        description="Current Redux interaction form state; sent so the Edit tool can diff against it",
    )


class ChatResponse(BaseModel):
    """Outbound response returned to the frontend."""

    reply: str = Field(
        ...,
        description="AI assistant's natural language reply",
    )
    tool_used: str | None = Field(
        default=None,
        description="Name of the LangGraph tool that was invoked (if any)",
    )
    form_data: dict | None = Field(
        default=None,
        description="Structured interaction data for Redux updateInteraction()",
    )
    interaction_id: str | None = Field(
        default=None,
        description="UUID of the created or updated interaction",
    )
