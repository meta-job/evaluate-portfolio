from uuid import uuid4
from ...database.MySQL import MySQL
from passlib.context import CryptContext
from ..schema.UserSchema import UserSchema
from fastapi.security import OAuth2PasswordBearer

class User():
    def __init__(self, request, url=None) -> None:
        self.request = request
        self.url = url
        self.msg = None
        self.mysql = MySQL()
        self.result = {}

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.mysql.close()

    def __enter__(self):
        if self.url == "signup":
            self.register(user=self.request)
            self.msg = "성공"

        elif self.url == "sign_in":
            pass

        elif self.url == "logout":
            pass

        elif self.url == "mypage":
            pass

        self.result['url'] = self.url
        self.result['msg'] = self.msg

        return self.result
    

    def register(self, user: UserSchema):
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        user_id = uuid4()
        query = f'''
            INSERT INTO metajob.user(user_id, user_name, user_email, user_password, user_phone, user_use)
            VALUES (
                '{user_id}',
                '{user.user_name}',
                '{user.user_email}',
                '{pwd_context.hash(user.user_password)}',
                '{user.user_phone}',
                1
            )
        '''
        self.mysql.insert_table(query)