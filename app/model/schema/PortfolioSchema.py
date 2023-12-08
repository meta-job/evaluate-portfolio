from pydantic import BaseModel, validator, EmailStr
from uuid import uuid4
from typing import List

class PortFolioSchema(BaseModel):
    portfolio_title: str 
    project_description: str


