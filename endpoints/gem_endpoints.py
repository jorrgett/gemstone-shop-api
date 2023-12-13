
from typing import List, Optional
from fastapi import APIRouter, Query
from models.gem_models import GemTypes
from repos.gem_repository import select_all_gems

gem_router = APIRouter()

@gem_router.get('/')
def greet():
    return 'Hello production'

@gem_router.get('/gems', tags=['Gems'])
def gems(lte: Optional[int] = None, gte: Optional[int] = None, type: List[Optional[GemTypes]] = Query(None)):

    gems = select_all_gems(lte, gte, type)
    return gems