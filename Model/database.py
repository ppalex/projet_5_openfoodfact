import mysql.connector
import Configuration.config as config

config.load('./configuration/config.yml')


class Database:
    _instance = None

    def __new__(self):
        """This method create an instance of Database.

        Returns:
            [Object] -- Database object.
        """
        if not self._instance:
            self._instance = super(Database, self).__new__(self)
            self.db = mysql.connector.connect(
                host=config.value['DB']['host'],
                user=config.value['DB']['user'],
                password=config.value['DB']['password'],
                database=config.value['DB']['database'],
                auth_plugin='mysql_native_password')

        return self._instance
