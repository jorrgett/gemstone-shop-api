from fastapi import FastAPI
from app.endpoints.gem_endpoints import gem_router
from app.endpoints.user_endpoints import user_router
from app.endpoints.seller_endpoints import seller_router
from app.models.gem_models import *

app = FastAPI()

app.include_router(user_router)
app.include_router(gem_router)
app.include_router(seller_router)