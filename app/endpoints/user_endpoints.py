from fastapi import APIRouter, HTTPException, Depends, status, Body
from starlette.responses import JSONResponse
from starlette.status import HTTP_201_CREATED
from app.auth.auth import AuthHandler
from app.db.db import session
from app.models.user_models import LoginInResponse, UserInput, User, UserLogin
from app.repos.user_repository import login_response, select_all_users, find_user

user_router = APIRouter()
auth_handler = AuthHandler()

@user_router.post('/registration', status_code=201, tags=['Users'], summary='Register new user')
def register(user: UserInput):
    """
    Register a new user.

    Parameters:
    - **user**: The input data for user registration.
        - **username**: The username for the new user. It should be unique.
        - **password**: The password for the new user.
        - **password2**: The confirmation of the password to ensure correctness.
        - **email**: The email address of the new user.
        - **is_seller**: A boolean indicating whether the user is a seller or not.

    Returns:
    - JSON response containing the details of the created user.

    Raises:
    - HTTPException 400: If the username is already taken or if there are validation errors.
    """
    users = select_all_users()

    if any(x.username == user.username for x in users):
        raise HTTPException(status_code=400, detail='Username is taken')
    
    hashed_pwd = auth_handler.get_password_hash(user.password)

    u = User(username=user.username, password=hashed_pwd, email=user.email,
             is_seller=user.is_seller)
    
    session.add(u)
    session.commit()

    created_user = {
        "username": u.username,
        "email": u.email,
        "is_seller": u.is_seller,
    }

    return JSONResponse(status_code=HTTP_201_CREATED, content=created_user)

@user_router.post(
        path='/login',
        tags=['Users'],
        response_model=LoginInResponse,
        status_code=status.HTTP_200_OK
)
def login(
    user: UserLogin = Body(...) 
):
    """
    Authenticate a user and generate an access token.

    Parameters:
    - **user**: The input data for user login.
        - **username**: The username of the user attempting to log in.
        - **password**: The password provided for authentication.

    Returns:
    - JSON response containing the authentication token.

    Raises:
    - HTTPException 401: If the username or password is invalid.
    """
    user_data = login_response(user, auth_handler)
    return user_data

@user_router.post('/forgot-password', tags=['Users'], summary='Request password reset')
async def forgot_password(user_email: str = Body(...)):
    """
    Request a password reset for the user with the given email.

    Parameters:
    - **user_email**: The email address of the user who wants to reset the password.

    Returns:
    - JSON response indicating that the password reset request has been processed.
    """
    # Implement the logic to send a password reset email or token
    # You might want to send an email to the user with a link containing a token for password reset
    # Ensure that you handle potential errors, like if the email doesn't exist in your system

    return {"message": "Password reset request processed. Check your email for further instructions."}


@user_router.post('/reset-password', tags=['Users'], summary='Reset password')
async def reset_password_route(
    token: str = Body(...),
    new_password: str = Body(...),
):
    """
    Reset the password using the provided reset token.

    Parameters:
    - **token**: The token received by the user for password reset.
    - **new_password**: The new password to set for the user.

    Returns:
    - JSON response indicating that the password has been successfully reset.
    """
    # Implement the logic to verify the token and update the user's password
    # Ensure that you handle potential errors, like an expired or invalid token

    reset_password = True

    reset_success = reset_password(token, new_password)

    if reset_success:
        return {"message": "Password has been successfully reset."}
    else:
        return {"message": "Password reset failed. Please try again."}


@user_router.get('/users/me', tags=['Users'])
def get_current_user(user: User = Depends(auth_handler.get_current_user)):
    """
    Get information about the current authenticated user.

    Returns:
    - JSON response containing user details.
    """
    return user