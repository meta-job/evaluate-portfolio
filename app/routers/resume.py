from fastapi import APIRouter, Form
from ..ai_util.ResumeEditor import ResumeEditor
from fastapi.encoders import jsonable_encoder
from starlette.background import BackgroundTask

router = APIRouter(
    prefix="/resume",
    tags=["portfolio"]
)

@router.get("/result")
def analysis_project(project_skill: str=Form("project_skill"), project_description: str=Form("project_description")):
    request = {"project_skill": project_skill, "project_description": project_description}

    try:
        with ResumeEditor(request=request) as result :
            return {"result": result}
        
    except Exception as e:
        return jsonable_encoder({"error": str(e)})