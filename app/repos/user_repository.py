from fastapi import HTTPException
from sqlmodel import Session, select

from app.db.db import engine
from app.models.user_models import User, LoginInResponse, UserLogin


def select_all_users():
    with Session(engine) as session:
        statement = select(User)
        res = session.exec(statement).all()
        return res

def find_user(name):
    with Session(engine) as session:
        statement = select(User).where(User.username == name)
        return session.exec(statement).first()
    
def login_response(user_login, auth_handler):

    user_found = find_user(user_login.username)

    if not user_found:
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    
    verified = auth_handler.verify_password(user_login.password, user_found.password)

    if not verified:
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    
    token = auth_handler.encode_token(user_found.username)

    return LoginInResponse(
        auth_credentials={'access_token': token, 'token_type': 'Bearer'},
        auth_info=user_login,
        user=find_user(user_login.username)
    )