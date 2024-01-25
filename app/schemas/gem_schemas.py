from pydantic import BaseModel
from app.models.gem_models import *

class CreateGem(BaseModel):
    quantity: int
    gem_type: Optional[GemTypes]

class CreateGemProperties(BaseModel):
    size: float = Field(..., gt=0)
    clarity: GemClarity
    color: GemColor

class UpdateGem(BaseModel):
    available: bool