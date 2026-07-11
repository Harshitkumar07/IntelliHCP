"""
LangGraph tool registry.

Exports the complete list of tools for binding to the LLM
and registering with ToolNode. Adding a new tool requires
only importing it here — zero changes to graph logic.
"""

from app.tools.log_interaction import log_interaction
from app.tools.edit_interaction import edit_interaction
from app.tools.search_doctor import search_doctor
from app.tools.recommend_products import recommend_products
from app.tools.plan_followup import plan_followup

# Ordered list — this is what gets bound to the LLM and ToolNode
ALL_TOOLS = [
    log_interaction,
    edit_interaction,
    search_doctor,
    recommend_products,
    plan_followup,
]

__all__ = [
    "ALL_TOOLS",
    "log_interaction",
    "edit_interaction",
    "search_doctor",
    "recommend_products",
    "plan_followup",
]
