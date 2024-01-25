from typing import Dict
from fastapi import HTTPException
from starlette.status import HTTP_404_NOT_FOUND
from fastapi.encoders import jsonable_encoder
from app.db.db import engine
from app.models.gem_models import Gem, GemProperties
from sqlmodel import Session, select
from app.populate import *
from app.schemas.gem_schemas import *

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
        image = generate_image(gem)

        gem_ = Gem(price=price, available=True, gem_type=gem.gem_type, image=image, gem_properties=gem_properties, quantity=gem.quantity)
        session.add(gem_)
        session.commit()

        # Recuperar la gema y sus propiedades después de ser agregada y confirmada
        session.refresh(gem_)
        session.refresh(gem_properties)

        return {'gem': gem_, 'props': gem_properties}
    
def updating_gem(id, gem):
    with Session(engine) as session:
        gem_found = session.get(Gem, id)

        if gem_found is None:
                raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f'Gem with ID {id} not found')

        gem_found.available = gem.available

        if gem_found.available == False:
            gem_found.quantity = 0

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