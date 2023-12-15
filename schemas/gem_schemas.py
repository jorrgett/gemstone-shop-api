from pydantic import BaseModel
from models.gem_models import *

class CreateGem(BaseModel):
    available: bool
    gem_type: Optional[GemTypes]

class CreateGemProperties(BaseModel):
    size: float = Field(..., gt=0)
    clarity: GemClarity
    color: GemColor

class UpdateGem(BaseModel):
    available: bool