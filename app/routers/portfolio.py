from fastapi import APIRouter, Form, File, UploadFile
from ..ai_util.portfolioEditor import PortfolioEditor
from fastapi.encoders import jsonable_encoder
from starlette.background import BackgroundTask
import os

router = APIRouter(
    prefix="/portfolio",
    tags=["portfolio"]
)

@router.get("/result")
def analysis_project(
    project_skill: str=Form("project_skill"), 
    project_description: str=Form("project_description"),
    portfolio_file: UploadFile = Form("portfolio_file"),
    user_id: str = Form("user_id")):

    upload_dir = f"files/{user_id}"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    file_path = os.path.join(upload_dir, portfolio_file.filename)
    with open(file_path, "wb") as f:
        f.write(portfolio_file.file.read())

    request = {"project_skill": project_skill, 
               "project_description": project_description,
               "portfolio_file": file_path
               }

    try:
        with PortfolioEditor(request=request) as result :
            return {"result": result}
        
    except Exception as e:
        return jsonable_encoder({"error": str(e)})