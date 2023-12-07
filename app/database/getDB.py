import os
from dotenv import load_dotenv

load_dotenv(verbose=True)

def func_getDBInfo(db_name = "metajob"):
    result = {"user":"metajob",    "password": os.getenv("DBPASSWORD"),  "port":7780, "host": "221.163.19.218"}
    return result