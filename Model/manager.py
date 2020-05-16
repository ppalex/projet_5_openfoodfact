from database import Database

class DatabaseManager(Database):
    def __init__(self):
        super()
    
    def get_db(self):
        return self.db
    
    def cursor(self, dic=False):
        return self.db.cursor(dictionary=dic)

    def commit(self):
        self.db.commit()

    def close(self):
        self.cursor.close()