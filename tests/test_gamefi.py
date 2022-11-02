import pytest
from web3 import Web3

from abi.gamefi import RaceABI
from api.gamefi import GamefiAPI
from common.constants import APIRespStatus, ContractRespStatus
from common.database import GamefiDatabase
from utility.time import wait_until_equals

class TestCase:

    gamefi_db = GamefiDatabase()
    gamefi_api = GamefiAPI()
    gamefi_race_abi = RaceABI()

    @pytest.mark.parametrize("address, private_key, message, signature", [
        ("0xFakeAddress", "fakePrivateKey", "fakeMessage", "fakeSignature")
    ])
    def test_dex_buy_vehicle(self, address, private_key, message, signature):
        res = self.gamefi_race_abi.buyVehicle(
            address=address,
            private_key=private_key,
            message=message,
            signature=signature
        )
        assert res['status'] == ContractRespStatus.SUCCESS, f"Mint failed, {res}"
        ...

    @pytest.mark.parametrize("address, private_key", [
        ("0xFakeAddress", "fakePrivateKey"),
    ])
    def test_cex_buy_vehicle(self, address, private_key):
        res = self.gamefi_api.mint_sign(
            miner_address=address
        ).json()
        assert res['code'] == APIRespStatus.SUCCESS, res
        message, signature = res['message'], res['signature']

        res = self.gamefi_race_abi.buyVehicle(
            address=address,
            private_key=private_key,
            message=message,
            signature=signature
        )
        mint_tx_hash = Web3.toHex(res['transactionHash'])
        assert res['status'] == ContractRespStatus.SUCCESS, f"Mint failed, {res}"
        assert wait_until_equals(
            lambda_func=lambda: self.gamefi_db.get_vehicle_mint_history(wallet_address=address)['mint_tx_hash'],
            expected=mint_tx_hash
        )