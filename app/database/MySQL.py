import pymysql
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
        except:
            self.conn.rollback()
    

    def read_table(self, query = ""):
        result = None
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
        except:
            self.conn.rollback()

        return result

    def read_dataframe(self, query = ""):
        result = None
        try:
            result = pd.read_sql(query, self.conn)
        except:
            self.conn.rollback()

        return result