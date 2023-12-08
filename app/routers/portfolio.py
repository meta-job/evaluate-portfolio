from fastapi import APIRouter, Form, File, UploadFile, Depends
from ..model.model.Portfolio import Portfolio
from fastapi.encoders import jsonable_encoder
from starlette.background import BackgroundTask
import os
from uuid import uuid4

router = APIRouter(
    prefix="/portfolios",
    tags=["portfolio"]
)

@router.get("/result")
def analysis_project(user_id: str=Form("user_id"),
                     portfolio_title: str=Form("portfolio_title"),
                     project_description: str=Form("project_description"),
                     portfolio_file: UploadFile = File("portfolio_file")):


    upload_dir = f"files/{user_id}"
    file_path = ""
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    if portfolio_file is not None and portfolio_file.filename is not "":
        file_name = f'{str(uuid4())}.pdf'
        file_path = os.path.join(upload_dir, file_name)

        with open(file_path, "wb") as f:
            f.write(portfolio_file.file.read())

    request = {"project_description": project_description,
               "portfolio_file": file_path if portfolio_file else "",
               "portfolio_title": portfolio_title, 
               "user_id": user_id
               }


    try:
        with Portfolio(request=request, url="portfolio") as result :
            return {"result": result}
        
    except Exception as e:
        return jsonable_encoder({"error": str(e)})