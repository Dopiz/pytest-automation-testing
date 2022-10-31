from configurations import GamefiConfig

from .database import Database


class GamefiDatabase(Database):

    def __init__(self):
        super().__init__(GamefiConfig.DATABASE)

    def get_vehicle_mint_history(self, wallet_address: str):
        args = {
            'wallet_address': wallet_address
        }
        sql = (
            """
            SELECT * 
            FROM vehicle_mint_history 
            WHERE wallet_address = %(wallet_address)s
            ORDER BY db_create_time DESC;
            """
        )
        res = self._connection.execute_select_sql(sql, args)
        return res
