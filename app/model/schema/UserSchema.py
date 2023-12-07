from pydantic import BaseModel, validator, EmailStr
from uuid import uuid4


class UserSchema(BaseModel):
    user_id: str = None
    user_email: EmailStr
    user_name: str
    user_password: str
    user_password_confirm: str
    user_phone: str
    user_use: int = 1

    @validator('user_email', 'user_password', 'user_name', pre=True, always=True)
    def empty_check(cls, v):
        if len(v) == 0 or v.strip() == "user_name":
            raise ValueError('empty value is not available')
        return v

    @validator('user_password_confirm')
    def password_match(cls, v, values):
        if 'user_password' in values and v != values['user_password']:
            raise ValueError('password does not match')
        return v
    
    @validator('user_id', pre=True, always=True)
    def set_user_id(cls, v):
        return v or str(uuid4())