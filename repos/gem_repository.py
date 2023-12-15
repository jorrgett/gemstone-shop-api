from typing import Dict
from fastapi.encoders import jsonable_encoder
from db.db import engine
from models.gem_models import Gem, GemProperties
from sqlmodel import Session, select
from populate import calculate_gem_price
from schemas.gem_schemas import *

def select_all_gems(lte, gte, type):
    with Session(engine) as session:
        statement = select(Gem, GemProperties).join(GemProperties)
        # statement = statement.where(Gem.id > 0).where(Gem.id < 2)
        # statement = statement.where(or_(Gem.id>1, Gem.price!=2000))

        if lte:
            statement = statement.where(Gem.price <= lte)
        if gte:
            statement = statement.where(Gem.price >= gte)
        if type:
            statement = statement.where(Gem.gem_type.in_(type)).order_by(Gem.gem_type).order_by(-Gem.price).order_by(None)

        result = session.exec(statement)
        res = []
        for gem, props in result:
            res.append({'gem': gem, 'props': props})
        return res

def select_gem(id):
    with Session(engine) as session:
        statement = select(Gem, GemProperties).join(GemProperties)
        statement = statement.where(Gem.id==id)
        result = session.exec(statement)
        res = []
        for gem, props in result:
            res.append({'gem': gem, 'props': props})
        return res
    
def create_gem(gem_pr: CreateGemProperties, gem: CreateGem) -> Dict[str, any]:
    with Session(engine) as session:
        gem_properties = GemProperties(size=gem_pr.size, clarity=gem_pr.clarity, color=gem_pr.color)
        session.add(gem_properties)
        session.commit()

        price = calculate_gem_price(gem, gem_pr)

        gem_ = Gem(price=price, available=gem.available, gem_type=gem.gem_type, gem_properties=gem_properties)
        session.add(gem_)
        session.commit()

        # Recuperar la gema y sus propiedades después de ser agregada y confirmada
        session.refresh(gem_)
        session.refresh(gem_properties)

        return {'gem': gem_, 'props': gem_properties}
    
def updating_gem(id, gem):
    with Session(engine) as session:
        gem_found = session.get(Gem, id)
        update_item_encoded = jsonable_encoder(gem)
        update_item_encoded.pop('id', None)
        for key, val in update_item_encoded.items():
            gem_found.__setattr__(key, val)
        session.commit()
        session.refresh(gem_found)
        return gem_found
    
def deleting_gem(id):
    with Session(engine) as session:
        gem_found = session.get(Gem, id)
        session.delete(gem_found)
        session.commit()

        return {"detail": "Gem deleted from the database"}

# select_gems()