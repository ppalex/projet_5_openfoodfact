from Model.manager import DatabaseManager


def initialize_job():

    db_manager = DatabaseManager()
    db_manager.create_tables()
    db_manager.close_conn()


def drop_tables_job():
    db_manager = DatabaseManager()
    db_manager.drop_tables()
