import pymysql
import pytds


class Database(object):

    def __init__(self, user, pwd, host, port, database):
        self.user = user
        self.pwd = pwd
        self.host = host
        self.port = int(port)
        self.database = database
        self._cursor = self._connect_database()

    def _connect_database(self):
        raise NotImplementedError("Do not use \'Database\' object.")

    def execute_modify_sql(self, sql: str, args: dict = None):
        try:
            res = self._cursor.execute(sql, args)
            self._connection.commit()
            return res
        except Exception as e:
            print(f"Modify Error: {e}")
            self._connection.rollback()
            return None

    def execute_select_sql(self, sql: str, args: dict = None, fetchall: bool = False):
        try:
            self._cursor.execute(sql, args)
            if fetchall:
                res = self._cursor.fetchall() or []
            else:
                res = self._cursor.fetchone()
            self._connection.commit()
            return res
        except Exception as e:
            print(f"Query Error: {e}")
            return None

    def __del__(self):
        self._connection.close()


class MsSqlDatabase(Database):

    def _connect_database(self):
        try:
            self._connection = pytds.connect(
                dsn=self.host,
                port=self.port,
                user=self.user,
                password=self.pwd,
                database=self.database,
                as_dict=True
            )
            # print(f"Connect to MsSql Database: {self.host}")
            return self._connection.cursor()
        except Exception as e:
            print(f"MsSQL Connect Fail: {e}")
            return None


class MySqlDatabase(Database):

    def _connect_database(self):
        try:
            self._connection = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.pwd,
                database=self.database,
                cursorclass=pymysql.cursors.DictCursor
            )
            # print(f"Connect to MySql Database: {self.host}")
            return self._connection.cursor()
        except Exception as e:
            print(f"MySQL Connect Fail: {e}")
            return None
