from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from models.gem_models import GemTypes
from repos.gem_repository import *
from starlette.responses import JSONResponse
from starlette.status import HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_200_OK

gem_router = APIRouter()

@gem_router.get('/')
def greet():
    return 'Hello production'

@gem_router.get('/gems/all', tags=['Gems'], summary="Retrieve gems based on specified criteria")
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

@gem_router.post('/gems/create', tags=['Gems'], summary="Create a new gem")
def create_gems(
    gem_pr: CreateGemProperties,
    gem: CreateGem
):
    """
    Create a new gem.

    Parameters:
    - **gem_pr**: The properties of the gem.
    - **gem**: The details of the gem.

    Raises:
    - **HTTPException 400 (Bad Request)**: If there is an issue creating the gem.

    Returns:
    - The created gem and its properties.

    Response:
    ```json
    {
        "gem_pr": {
            "size": 4.4,       # Size of the gem in carats
            "clarity": 3,      # Clarity rating of the gem (SI, VS, VVS, FL)
            "color": "G"       # Color grade of the gem (D, E, G, F, H, I)
        },
        "gem": {
            "available": true,       # Availability status of the gem
            "gem_type": "RUBY",      # Type of gem (e.g., RUBY, DIAMOND, EMERALD, etc.)
        }
    }
    ```
    - **Clarity Rating:**
        - 1 (SI): Slightly Included
        - 2 (VS): Very Slightly Included
        - 3 (VVS): Very, Very Slightly Included
        - 4 (FL): Flawless
    - **Color Grade:**
        - 'D': Colorless ++
        - 'E': Colorless +
        - 'F': Colorless
        - 'G': Near-Colorless 
        - 'H': Near-Colorless -
        - 'I': Near-Colorless --
    """
    try:
        created_gem = create_gem(gem_pr, gem)
        return created_gem
    except Exception as e:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail='Invalid parameters sent to the database')

@gem_router.put('/gems/{id}', tags=['Gems'], summary="Update Gem Availability")
def update_gem(id: int, gem: UpdateGem):
    """
    Update the availability status of a gem identified by its unique identifier.

    Parameters:
    - **id**: The unique identifier of the gem.
    - **gem**: The details to be updated for the gem's availability.

    Request Body:
    ```json
    {
        "available": true
    }
    ```

    Raises:
    - **HTTPException 400 (Bad Request)**: If there is an issue updating the gem.
    - **HTTPException 404 (Not Found)**: If the gem with the specified ID is not found.

    Returns:
    - The updated details of the gem.

    Example:
    ```http
    PUT /gems/398
    ```

    Request Body:
    ```json
    {
        "available": false
    }
    ```

    Response:
    ```json
    {
        "gem_type": "RUBY",
        "available": false,
        "id": 398,
        "price": 129600,
        "gem_properties_id": 398
    }
    ```
    """
    try:
        gem_found_ = updating_gem(id, gem)
        return gem_found_
    except Exception as e:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail='Invalid parameters sent to the database')

@gem_router.delete('/gems/{id}',status_code=HTTP_204_NO_CONTENT, tags=['Gems'])
def delete_gem(id: int):
    """
    Delete a gem identified by its unique identifier.

    Parameters:
    - **id**: The unique identifier of the gem to be deleted.

    Raises:
    - **HTTPException 404 (Not Found)**: If the gem with the specified ID is not found.
    - **HTTPException 400 (Bad Request)**: If there is an issue deleting the gem.

    Returns:
    - No content (HTTP 204 No Content) if the deletion is successful.

    Example:
    ```http
    DELETE /gems/123
    ```

    Response:
    ```http
    HTTP/1.1 204 No Content
    ```
    """
    try:
        delete = deleting_gem(id)
        return delete
    except Exception as e:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail='Invalid parameters sent to the database')