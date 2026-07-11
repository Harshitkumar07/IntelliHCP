"""
API v1 router — aggregates all v1 endpoint routers.

Adding a new resource = import its router and include it here.
"""

from __future__ import annotations

from fastapi import APIRouter

from app.api.v1.chat import router as chat_router
from app.api.v1.interactions import router as interactions_router

router = APIRouter()

router.include_router(chat_router)
router.include_router(interactions_router)
