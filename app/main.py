from fastapi import FastAPI, Form, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from .routers import portfolio
from .routers import user
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from uuid import uuid4
import os
from dotenv import load_dotenv



import pymysql
from .model.schema.UserSchema import UserSchema, UserLogin
from .model.model.User import User

from .database.MySQL import MySQL

import logging


load_dotenv()
app = FastAPI()


app.include_router(portfolio.router)
app.include_router(user.router)

@app.get("/")
def root():
    return {"Hello": "World"}

@app.post("/signup")
def signup(
    user_name: str = Form("user_name"),
    user_email: str = Form("user_email"),
    user_password: str = Form("user_password"),
    user_password_confirm: str = Form("user_password_confirm"),
    user_phone: str = Form("user_phone"),
    ):
    user_phone = "" if user_phone.strip() == "user_phone" else user_phone
    request = UserSchema(
        user_name=user_name,
        user_email=user_email,
        user_password=user_password,
        user_password_confirm=user_password_confirm,
        user_phone=user_phone,
    )
    try:
        with User(request=request, url="signup") as user:
            return user
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code = 500)

@app.post("/signin", response_model = UserLogin)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    with User(request=form_data, url = "signin") as user:
        return user["token"]