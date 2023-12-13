
from typing import List, Optional
from fastapi import APIRouter, Query
from models.gem_models import GemTypes
from repos.gem_repository import select_all_gems

gem_router = APIRouter()

@gem_router.get('/')
def greet():
    return 'Hello production'

@gem_router.get('/gems', tags=['Gems'], summary="Retrieve gems based on specified criteria")
def gems(
    lte: Optional[int] = Query(None, description="Filter gems with a value less than or equal to this"),
    gte: Optional[int] = Query(None, description="Filter gems with a value greater than or equal to this"),
    type: List[Optional[GemTypes]] = Query(None, description="Filter gems by type (diamond, ruby, emerald)")
):
    """
    Retrieve a list of gems based on specified criteria.

    Parameters:
    - **lte**: Filter gems with a value less than or equal to this.
    - **gte**: Filter gems with a value greater than or equal to this.
    - **type**: Filter gems by type (diamond, ruby, emerald).

    Returns:
    - List of gems that match the specified criteria.
    """
    gems = select_all_gems(lte, gte, type)
    return gems