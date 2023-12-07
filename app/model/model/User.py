from uuid import uuid4
from ...database.MySQL import MySQL
from passlib.context import CryptContext
from ..schema.UserSchema import UserSchema
from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import timedelta, datetime
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


class User():
    def __init__(self, request, url=None) -> None:
        self.request = request
        self.url = url
        self.msg = None
        self.mysql = MySQL()
        self.result = {}
        self.password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.mysql.close()

    def __enter__(self):
        if self.url == "signup":
            self.msg = self.register()

        elif self.url == "signin":
            self.signin()

        elif self.url == "logout":
            pass

        elif self.url == "mypage":
            pass

        self.result['url'] = self.url
        self.result['msg'] = self.msg

        return self.result
    

    def register(self):
        user = self.request
        if self.get_user_by_email():
            return {"error": "user email already exists"}


        user_id = uuid4()
        query = f'''
            INSERT INTO metajob.user(user_id, user_name, user_email, user_password, user_phone, user_use)
            VALUES (
                '{user_id}',
                '{user.user_name}',
                '{user.user_email}',
                '{self.password_context.hash(user.user_password)}',
                '{user.user_phone}',
                1
            )
        '''
        self.mysql.insert_table(query)

    def signin(self):
        user = self.get_user_by_email_for_login()
        if not user or not self.verify_password(self.request.password, user["user_password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        access_token = self.create_jwt_token({"sub": self.request.username})

        self.result["token"] = {
            "access_token": access_token,
            "token_type": "bearer",
            "user_email":  user["user_email"]
        }
    
    def get_user_by_email(self):
        user = self.request
        query = f'''
                SELECT user_email, user_password
                FROM metajob.user
                WHERE user_email ='{user.user_email}'
                '''
        
        result = self.mysql.read_data(query=query)
        return result[0]

    def get_user_by_email_for_login(self):
        user = self.request
        query = f'''
                SELECT user_email, user_password
                FROM metajob.user
                WHERE user_email ='{user.username}'
                '''
        
        result = self.mysql.read_data(query=query)
        return result[0]


    def verify_password(self, plain_password, hashed_password):
        return self.password_context.verify(plain_password, hashed_password)
    
    def create_jwt_token(self, data: dict):
        to_encode = data.copy()
        expire = 60*15
        to_encode.update({"exp": timedelta(minutes=expire) + datetime.utcnow()})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)
        return encoded_jwt

    def signout(self):
        pass