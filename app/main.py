from fastapi import FastAPI, Form, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from .routers import portfolio
from .routers import user
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from uuid import uuid4

import pymysql

from .model.schema.UserSchema import UserSchema
from .model.model.User import User

from .database.MySQL import MySQL

import logging

app = FastAPI()

app.include_router(portfolio.router)
app.include_router(user.router)

@app.get("/")
def root():
    return {"Hello": "World"}

mysql_instance = MySQL()

@app.get("/db")
def db():
    connection = pymysql.connect(
        host="221.163.19.218",
        user="metajob",
        password="1q2w3e4r5t",
        port=7780,
        cursorclass=pymysql.cursors.DictCursor,
        db="metajob"
    )
    try:
        with connection.cursor() as cursor:
            sql = f"INSERT INTO metajob.user(user_id, user_email, user_name, user_password, user_phone, user_use) VALUES('{uuid4()}', 'jean', 'jean', 'jean' ,'jean', 1) "
            result = cursor.execute(sql)
        connection.commit()
        return {"message": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        connection.close()  

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
        