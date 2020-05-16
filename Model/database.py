import mysql.connector
import Configuration.config as config

config.load('./configuration/config.yml')


class Database:
    _instance = None

    def __new__(self):
        if not self._instance:
            self._instance = super(Database, self).__new__(self)
            self.db = mysql.connector.connect(
                host=config.value['DB']['host'],
                user=config.value['DB']['user'],
                password=config.value['DB']['password'],
                database=config.value['DB']['database'],
                auth_plugin='mysql_native_password')

        return self._instance

    @classmethod
    def get_db(cls):
        return cls()

    def cursor(self, dic=False):
        return self.db.cursor(dictionary=dic)

    def commit(self):
        self.db.commit()

    def close_cur(self):
        self.cursor.close()

    def close_conn(self):
        self.db.close()
