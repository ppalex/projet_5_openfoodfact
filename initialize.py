from Model.database import Database
from Model.manager import DatabaseManager

import pdb


def initialize_job():
    db = Database.get_db()
    
    db_manager = DatabaseManager()
    pdb.set_trace()
    db_manager.create_tables()
    
    db.close_conn()
