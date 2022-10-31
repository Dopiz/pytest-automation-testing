from utility.database import MsSqlDatabase, MySqlDatabase


class Database:

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, config):
        self.config = config
        self.__connection = None

    @property
    def _connection(self):
        if self.__connection is None:
            user = self.config.user
            pwd = self.config.password
            host = self.config.host
            port = self.config.port
            database = self.config.database
            db = {
                'mssql': MsSqlDatabase,
                'mysql': MySqlDatabase
            }.get(self.config.driver.lower())
            self.__connection = db(user, pwd, host, port, database)
        return self.__connection

    @staticmethod
    def select(table: str, fields: list = None, condition: list = None):
        if fields is None or not len(fields):
            fields = "*"
        else:
            fields = ', '.join(fields)
        sql = (f"SELECT {fields} FROM {table} ")
        if condition:
            condition = ' AND '.join(f"{field} = %({field})s" for field in condition)
            sql += (f"WHERE {condition} ")
        return sql

    @staticmethod
    def update(table: str, fields: list, condition: list = None):
        fields = ', '.join(f"{field} = %({field})s" for field in fields)
        sql = (f"UPDATE {table} SET {fields} ")
        if condition:
            condition = ' AND '.join(f"{field} = %({field})s" for field in condition)
            sql += (f"WHERE {condition} ")
        return sql

    @staticmethod
    def remove_dict_empty_value(dict: dict):
        return {k: v for k, v in dict.items() if v is not None and v != ""}
