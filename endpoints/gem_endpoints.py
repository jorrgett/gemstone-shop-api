from typing import List, Optional
from fastapi import APIRouter, Query
from models.gem_models import GemTypes
from repos.gem_repository import *
from starlette.responses import JSONResponse
from starlette.status import HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED
from db.db import session

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

@gem_router.get('/gem/{id}', tags=['Gems'], summary="Retrieve a gem by ID")
def gem(id: int):
    """
    Retrieve information about a gem by its unique identifier.

    Parameters:
    - **id**: The unique identifier of the gem.

    Raises:
    - **HTTPException 404 (Not Found)**: If the gem with the specified ID is not found.

    Returns:
    - The details of the gem identified by the provided ID.

    Example:
    ```http
    GET /gem/400
    ```

    Response:
    ```json
    {
        "gem": {
        "available": true,
        "price": 106480,
        "id": 400,
        "gem_type": "RUBY",
        "gem_properties_id": 400
        },
        "props": {
        "size": 4.4,
        "clarity": 3,
        "color": "G",
        "id": 400
        }
    }
    ```
    """
    gem_found = select_gem(id)
    if not gem_found:
        error_response = {"detail": "Gem not found"}
        return JSONResponse(content=error_response, status_code=HTTP_404_NOT_FOUND)
    return gem_found
