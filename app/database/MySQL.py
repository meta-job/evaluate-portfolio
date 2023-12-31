import pymysql
from pymysql.cursors import DictCursor
import pandas as pd
from .getDB import func_getDBInfo

class MySQL:
    def __init__(self) -> None:
        self.db_name = "metajob"
        self.conn = self.get_db_conn()

    
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __enter__(self):
        return self.conn
    
    def close(self):
        return self.conn.close()
    
    def get_db_conn(self):
        accountInfo = func_getDBInfo()
        return pymysql.connect( user=accountInfo['user'], 
                                password=accountInfo['password'], 
                                host=accountInfo['host'],  
                                port=int(accountInfo['port']),
                                db=self.db_name
                              )
    
    def insert_table(self, query=""):
        try:
            cursor = self.conn.cursor()
            result = cursor.execute(query)
            self.conn.commit()
            return {"message": result}
        except Exception as e:
            self.conn.rollback()
            return {"error": str(e)}
    

    def read_table(self, query = ""):
        result = None
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
        except Exception as e:
            self.conn.rollback()
            return {"error": str(e)}
        return result

    def read_data(self, query = ""):
        result = None
        try:
            cursor = self.conn.cursor(DictCursor)
            cursor.execute(query)
            result = cursor.fetchall()
        except Exception as e:
            self.conn.rollback()
            return {"error": str(e)}
        return result