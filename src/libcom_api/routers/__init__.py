from typing import List

from fastapi import APIRouter
from loguru import logger

from .color_transfer import router as color_transfer_router
from .controllable_composition import router as controllable_composition_router
from .shadow_generation import router as shadow_generation_router

__all__ = [
    "color_transfer_router",
    "controllable_composition_router",
    "shadow_generation_router",
]


def gather_routers() -> List[APIRouter]:
    """Gather all routers.

    Returns:
        List[APIRouter]: List of routers.
    """
    routers = []
    for name in __all__:
        router = globals()[name]
        assert isinstance(router, APIRouter), router
        logger.info(f"Adding router `{name}`")
        routers.append(router)

    return routers
