import os
from dotenv import load_dotenv

load_dotenv(verbose=True)

def func_getDBInfo(db_name = ""):
    result = {"user":"metajob",    "password": os.getenv("DBPASSWORD"),  "port":7780,   "srv":False,    "host": "221.163.19.218"}
    # result = {
    #             "MongoDB_portfolio": {"user":"igniteofficial",    "password":"fi6sDClNZ4lykLBz",  "port":None,   "srv":True,       "host":"portfolio.64921qv.mongodb.net/?retryWrites=true&w=majority"},
    #          }.get(db_name, {"user":"ignitedb",    "password":"meIsPPcJ7epvCMa6",  "port":33306,   "srv":False,    "host":"211.177.37.136"})
    return result