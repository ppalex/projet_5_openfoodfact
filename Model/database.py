import mysql.connector

class Database:
    _instance = None
    def __new__(self):
        if not self._instance:
            self._instance  = super(Database, self).__new__(self)
            self.db = mysql.connector.connect(host='localhost',
                                              user='root',
                                              password='Ingestic13&',
                                              database='openfoodfact',
                                              auth_plugin='mysql_native_password')

        return self._instance

