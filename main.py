from fastapi import FastAPI
import uvicorn
from endpoints.gem_endpoints import gem_router
from endpoints.user_endpoints import user_router
from models.gem_models import *

app = FastAPI()

app.include_router(user_router)
app.include_router(gem_router)


# def create_db_and_tables():
#     SQLModel.metadata.create_all(engine)

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8001)
    #create_db_and_tables()