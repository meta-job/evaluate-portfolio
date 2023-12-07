from pydantic import BaseModel, validator, EmailStr
from uuid import uuid4


class PortFolioSchema(BaseModel):
    portfolio_num: str = None
    user_id: str
    portfolio_title: str
    portfolio_content: str
    portfolio_use : int = 1
    portfolio_file_path: str
    created_at: str
