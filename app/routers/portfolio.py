from fastapi import APIRouter, Request, Form, File, UploadFile, Depends
from ..model.model.Portfolio import Portfolio
from fastapi.encoders import jsonable_encoder
from starlette.background import BackgroundTask
from pydantic import BaseModel
from typing import List, Dict
import json
import os
from uuid import uuid4

router = APIRouter(
    prefix="/portfolios",
    tags=["portfolio"]
)


@router.post("/result")
def analysis_project(user_id: str = Form(...), portfolio_title: str=Form(...), project_description: list=Form(...)):


    # user_id = form_data.user_id
    # portfolio_title = form_data.portfolio_title
    # project_description = form_data.project_description


    # upload_dir = f"files/{user_id}"
    # file_path = ""

    # if not os.path.exists(upload_dir):
    #     os.makedirs(upload_dir)

    # if portfolio_file != "portfolio_file":
    #     file_name = f'{str(uuid4())}.pdf'
    #     file_path = os.path.join(upload_dir, file_name)

    #     with open(file_path, "wb") as f:
    #         f.write(portfolio_file.file.read())

    request = {"project_description": project_description,
               "portfolio_title": portfolio_title, 
               "user_id": user_id
               }

    try:
        with Portfolio(request=request, url="portfolio") as result :
            return result
        
    except Exception as e:
        return jsonable_encoder({"error": str(e)})