from uuid import uuid4
from ...database.MySQL import MySQL
from ...ai_util.portfolioEditor import PortfolioEditor
from fastapi import Depends, HTTPException, status
import json

class Portfolio():
    def __init__(self, request, url=None) -> None:
        self.request = request
        self.url = url
        self.msg = None
        self.mysql = MySQL()
        self.result = {}

    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.mysql.close()

    def __enter__(self):
        if self.url == "portfolio_list":
            pass
        elif self.url == "portfolio":
            self.make_and_insert_portfolio()

        self.result['url'] = self.url
        self.result['msg'] = self.msg

        return self.result
    
    def make_and_insert_portfolio(self):
        portfolio = ""
        with PortfolioEditor(self.request) as editor:
            portfolio = editor["answer"]
            
        if not portfolio:
            self.result["error"] = "portfolio 미생성"
        else:
            portfolio = json.dumps(portfolio, ensure_ascii=False)
            query = f'''
                INSERT INTO metajob.portfolio( portfolio_content, portfolio_title, portfolio_use, user_id, portfolio_file_path)
                VALUES (
                    '{portfolio}',
                    '{self.request["portfolio_title"]}',
                    1,
                    '{self.request["user_id"]}',
                    '{self.request["portfolio_file"]}'
                )
            '''
            self.msg= self.mysql.insert_table(query)

        self.result["result"] = portfolio
        