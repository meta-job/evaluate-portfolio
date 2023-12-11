from uuid import uuid4
from ...database.MySQL import MySQL
from ...ai_util.portfolioEditor import PortfolioEditor
from fastapi import Depends, HTTPException, status
import json
import ast
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
            self.get_list_portfolio()
        elif self.url == "portfolio":
            self.make_and_insert_portfolio()
        elif self.url == "my_portfolio":
            self.get_my_portfolio()

        self.result['url'] = self.url
        self.result['msg'] = self.msg

        return self.result
    
    def make_and_insert_portfolio(self):
        portfolio = {}
        
        with PortfolioEditor(self.request) as editor:
            portfolio = editor

        portfolio_content = portfolio["answer"]

        json_portfolio_content = {}
        for i in range(0, len(portfolio_content)):
            key = portfolio_content[i][0]
            json_content = portfolio_content[i][1].replace("\n", "")
            json_content = '{' + json_content.strip('\'') + '}'
            json_content = json.dumps(json_content)
            parsed_json = json.loads(json_content)
            json_portfolio_content[key] = ast.literal_eval(parsed_json)

        json_portfolio_content_result = json.dumps(json_portfolio_content, indent=2, ensure_ascii=False)

        portfolio_description = json.dumps(self.request["project_description"], ensure_ascii=False).replace("'", r"\'")

        portfolio_file_id = " "

        if not portfolio:
            self.result["error"] = "portfolio 미생성"
        else:
            query = f'''
                INSERT INTO metajob.portfolio( portfolio_content, portfolio_title, portfolio_description, portfolio_use, user_id, portfolio_file_id, created_at)
                VALUES (
                    '{json_portfolio_content_result}',
                    '{self.request["portfolio_title"]}',
                    '{portfolio_description}',
                    1,
                    '{self.request["user_id"]}',
                    '{portfolio_file_id}',
                    DATE(NOW())
                )
            '''
            self.msg= self.mysql.insert_table(query)

        self.result["result"] = {"title": self.request["portfolio_title"] ,"content": json_portfolio_content_result}
        
    def get_list_portfolio(self):
        if not self.request["user_id"]:
            self.request['msg'] = "user_id not exists"
        query = f'''
            SELECT * FROM metajob.portfolio WHERE user_id = '{self.request["user_id"]}'
        '''
        self.result["result"] = self.mysql.read_table(query=query)

    def get_my_portfolio(self):
        if not self.request["user_id"]:
            self.request['msg'] = "user_id not exists"
        if not self.request["portfolio_no"]:
            self.request['msg'] = "porfolio_no not exists"
        query = f'''
            SELECT * FROM metajob.portfolio WHERE user_id = '{self.request["user_id"]}' AND portfolio_no = {self.request["portfolio_no"]}
        ''' 
        self.result["result"] = self.mysql.read_data(query=query)