from abi.base_abi import BaseABI
from configurations import GeneralConfig, GamefiConfig


class RaceABI(BaseABI):

    def __init__(self):
        super().__init__(
            chain_id=GeneralConfig.BSC_CHAIN_ID,
            node_url=GeneralConfig.BSC_NODE_URL,
            config=GamefiConfig.RACE_CONTRACT
        )

    def buyHistory(self):
        return self._send_read_request(
            abi=self._contract.functions.buyHistory()
        )

    def buyVehicle(self, address: str, private_key: str, message: bytes, signature: bytes):
        return self._send_write_request(
            address=address,
            private_key=private_key,
            abi=self._contract.functions.buyVehicle(
                message=message,
                signature=signature,
            )
        )

    ...