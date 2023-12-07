from fastapi import APIRouter, Form
from ..ai_util.portfolioEditor import PortfolioEditor
from ..model.model.Portfolio import Portfolio

router = APIRouter(
    prefix="/mypage",
    tags=["mypage"]
)

@router.get("/portfolio_list")
def portfolio_list(user_id : str = Form("user_id")):
  request = {"user_id": user_id}
  with Portfolio(request=request, url="portfolio_list") as list:
    return list
  
@router.get("/my_portfolio/{portfolio_no}")
def portfolio_list( portfolio_no: int, user_id : str = Form("user_id")):
  request = {"user_id": user_id, "portfolio_no": portfolio_no}
  with Portfolio(request=request, url="my_portfolio") as list:
    return list
  
