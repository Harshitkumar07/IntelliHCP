"""
LangGraph agent — the core AI orchestration engine.

Architecture improvements integrated:
  1. Native ToolNode — LangGraph's prebuilt ToolNode handles tool execution
     automatically, eliminating custom tool executor code.
  2. tools_condition — LangGraph's prebuilt conditional edge function
     checks for tool_calls and routes accordingly.
  3. MemorySaver — checkpointer enables multi-turn conversation memory
     per session_id (thread_id). The agent remembers previous messages.
  4. Single extraction — the LLM extracts structured data ONCE in its
     tool_call arguments. Tools do purely deterministic work.

Graph Topology:
    START → llm_node → [tools_condition] → ToolNode → llm_node → ... → END
                              ↓ (no tool calls)
                             END

The cycle ToolNode → llm_node ensures the LLM sees tool results
and generates a human-readable confirmation message.
"""

from __future__ import annotations

from langchain_core.messages import SystemMessage
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from app.core.config import settings
from app.core.logging import get_logger
from app.graph.state import AgentState
from app.prompts.system import build_system_prompt
from app.tools import ALL_TOOLS

logger = get_logger(__name__)

# ── LLM Configuration ───────────────────────────────────
# Initialise once — reused across all graph invocations
llm = ChatGroq(
    api_key=settings.GROQ_API_KEY,
    model=settings.GROQ_MODEL,
    temperature=0.1,          # Low temp for consistent structured extraction
    max_tokens=2048,
)

# Bind tools to the LLM so it knows what tools are available
# and can generate tool_call messages with structured arguments
llm_with_tools = llm.bind_tools(ALL_TOOLS)


# ── Graph Nodes ──────────────────────────────────────────

def llm_node(state: AgentState) -> dict:
    """Invoke the Groq LLM with conversation history and tool bindings.

    This node:
      1. Constructs the system prompt (with dynamic form context)
      2. Prepends it to the conversation history
      3. Calls the LLM which either:
         a) Returns a tool_call message (routed to ToolNode)
         b) Returns a plain text message (routed to END)

    The system prompt is NOT stored in state — it's constructed fresh
    each time so the current_form context is always up-to-date.
    """
    messages = state["messages"]
    current_form = state.get("current_form") or {}

    # Build system prompt with dynamic form context
    system_prompt = build_system_prompt(current_form)
    system_message = SystemMessage(content=system_prompt)

    # Invoke LLM with system + conversation history
    response = llm_with_tools.invoke([system_message] + messages)

    logger.debug(
        "LLM response type: %s, has_tool_calls: %s",
        type(response).__name__,
        bool(getattr(response, "tool_calls", None)),
    )

    return {"messages": [response]}


# ── Graph Construction ───────────────────────────────────

def build_agent_graph() -> StateGraph:
    """Construct and compile the LangGraph agent.

    Returns a compiled graph with MemorySaver checkpointer
    for multi-turn conversation memory.

    Graph edges:
        START → llm_node
        llm_node → tools_condition → ToolNode (if tool_calls present)
        llm_node → tools_condition → END (if no tool_calls)
        ToolNode → llm_node (cycle back for confirmation message)
    """
    # Create the ToolNode with all registered tools
    tool_node = ToolNode(ALL_TOOLS)

    # Build the graph
    graph_builder = StateGraph(AgentState)

    # Add nodes
    graph_builder.add_node("llm_node", llm_node)
    graph_builder.add_node("tools", tool_node)

    # Add edges
    graph_builder.add_edge(START, "llm_node")

    # Conditional edge: if LLM returned tool_calls → ToolNode, else → END
    graph_builder.add_conditional_edges(
        "llm_node",
        tools_condition,
        # tools_condition returns "tools" if tool_calls present, END otherwise
    )

    # After tool execution, cycle back to LLM for confirmation message
    graph_builder.add_edge("tools", "llm_node")

    # Compile with MemorySaver for conversation persistence
    memory = MemorySaver()
    compiled_graph = graph_builder.compile(checkpointer=memory)

    logger.info("LangGraph agent compiled with %d tools and MemorySaver", len(ALL_TOOLS))

    return compiled_graph


# ── Singleton Agent ──────────────────────────────────────
# Compiled once at module load, reused across all requests
agent = build_agent_graph()
