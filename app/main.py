from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.endpoints.gem_endpoints import gem_router
from app.endpoints.user_endpoints import user_router
from app.endpoints.seller_endpoints import seller_router
from app.models.gem_models import *

app = FastAPI()

app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(user_router)
app.include_router(gem_router)
app.include_router(seller_router)