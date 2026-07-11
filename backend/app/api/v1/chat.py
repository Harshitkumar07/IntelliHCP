"""
Chat endpoint — the primary gateway between the React frontend
and the LangGraph agent.

This endpoint:
  1. Receives a natural language message + session_id + current_form
  2. Invokes the LangGraph agent with MemorySaver thread_id
  3. Extracts the agent's reply, tool_used, and form_data from the result
  4. Returns a structured ChatResponse for Redux consumption

WHY a thin endpoint?
  - All intelligence lives in the LangGraph agent
  - The endpoint only validates, invokes, and formats
  - Easy to test, easy to replace transport (WebSocket later)
"""

from __future__ import annotations

import json
import traceback

from fastapi import APIRouter, HTTPException
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage

from app.core.logging import get_logger
from app.graph.agent import agent
from app.schemas.chat import ChatRequest, ChatResponse

logger = get_logger(__name__)

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    """Process a chat message through the LangGraph agent.

    The agent uses MemorySaver keyed by session_id, so multi-turn
    conversations within the same session maintain full context.
    """
    logger.info(
        "Chat request — session: %s, message: %.100s",
        request.session_id,
        request.message,
    )

    try:
        # ── Build agent input ───────────────────────────
        input_state = {
            "messages": [HumanMessage(content=request.message)],
            "current_form": request.current_form or {},
        }

        # ── Invoke with MemorySaver thread ──────────────
        config = {
            "configurable": {
                "thread_id": request.session_id,
            }
        }

        result = agent.invoke(input_state, config)

        # ── Extract response from agent state ───────────
        reply, tool_used, form_data, interaction_id = _parse_agent_result(result)

        logger.info(
            "Chat response — tool: %s, has_form_data: %s",
            tool_used,
            form_data is not None,
        )

        return ChatResponse(
            reply=reply,
            tool_used=tool_used,
            form_data=form_data,
            interaction_id=interaction_id,
        )

    except Exception as exc:
        logger.error("Chat endpoint error: %s\n%s", str(exc), traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Agent error: {str(exc)}",
        ) from exc


def _parse_agent_result(result: dict) -> tuple[str, str | None, dict | None, str | None]:
    """Extract structured data from the LangGraph agent's final state.

    Walks backwards through messages to find:
      1. The last AI message (the reply text)
      2. The last tool message (tool_used + form_data)

    Returns:
        (reply, tool_used, form_data, interaction_id)
    """
    messages = result.get("messages", [])

    reply = "I'm sorry, I couldn't process that request."
    tool_used = None
    form_data = None
    interaction_id = None

    # Walk messages in reverse to find the final AI reply and tool result
    for msg in reversed(messages):
        if isinstance(msg, AIMessage) and not getattr(msg, "tool_calls", None):
            # This is the final conversational reply (not a tool-calling message)
            reply = msg.content
            break

    # Find the last tool message for form_data extraction
    for msg in reversed(messages):
        if isinstance(msg, ToolMessage):
            tool_used = msg.name
            try:
                tool_result = json.loads(msg.content)
                form_data = tool_result.get("form_data")
                interaction_id = tool_result.get("interaction_id")

                # Handle follow-up suggestions (from plan_followup tool)
                if "follow_up_suggestions" in tool_result and form_data is None:
                    form_data = {
                        "follow_up_suggestions": tool_result["follow_up_suggestions"]
                    }

                # Handle doctor search results (from search_doctor tool)
                if "doctors" in tool_result and form_data is None:
                    form_data = {
                        "search_results": tool_result["doctors"]
                    }

                # Handle product recommendations
                if "recommendations" in tool_result and form_data is None:
                    form_data = {
                        "recommendations": tool_result["recommendations"]
                    }

            except (json.JSONDecodeError, AttributeError):
                logger.warning("Could not parse tool message content as JSON")
            break

    return reply, tool_used, form_data, interaction_id
