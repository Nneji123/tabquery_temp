import os
from uuid import uuid4

from app.deps import get_current_user
from app.schemas import SystemUser, TokenSchema, UserAuth, UserOut
from app.utils import (create_access_token, create_refresh_token,
                       get_hashed_password, verify_password)
from fastapi import Depends, FastAPI, HTTPException, status, File, UploadFile
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from replit import db
from .utils import execute_query

app = FastAPI()

@app.get('/', response_class=RedirectResponse, include_in_schema=False)
async def docs():
    return RedirectResponse(url='/docs')


@app.post('/signup', summary="Create new user", response_model=UserOut)
async def create_user(data: UserAuth):
    # querying database to check if user already exist
    user = db.get(data.email, None)
    if user is not None:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
        )
    user = {
        'email': data.email,
        'password': get_hashed_password(data.password),
        'id': str(uuid4())
    }
    db[data.email] = user    # saving user to database
    return user


@app.post('/login', summary="Create access and refresh tokens for user", response_model=TokenSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.get(form_data.username, None)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    hashed_pass = user['password']
    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    
    return {
        "access_token": create_access_token(user['email']),
        "refresh_token": create_refresh_token(user['email']),
    }

@app.get('/me', summary='Get details of currently logged in user', response_model=UserOut)
async def get_me(user: SystemUser = Depends(get_current_user)):
    return user

@app.post("/query", tags=["table-query"], summary="Post query and get answer", response_model=UserOut)
async def get_table(question:str, user: SystemUser = Depends(get_current_user), file: UploadFile = File(...)):
    files = await file.read()
    # save the file
    filename = "filename.csv"
    with open(filename, "wb+") as f:
        f.write(files)
    # open the file and return the file name
    try:
        data = execute_query(question, "filename.csv")
        if os.path.exists("filename.csv"):
            os.remove("filename.csv")
        return data
    except ValueError as e:
        return {"error": str(e)}