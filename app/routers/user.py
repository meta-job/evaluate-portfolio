from fastapi import APIRouter, Form
from ..ai_util.portfolioEditor import PortfolioEditor

router = APIRouter(
    prefix="/mypage",
    tags=["mypage"]
)

@router.get("/{user_id}")
def mypage():
  pass