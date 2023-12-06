from fastapi import APIRouter
from ..ai_util.portfolioEditor import PortfolioEditor

router = APIRouter(
    prefix="/{user_id}",
    tags=["portfolio"]
)

@router.get("/portfolio_list")
def get_my_portfolio_list():
  pass

@router.get("/{portfolio_id}")
def get_my_portfolio():
    pass