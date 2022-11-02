import pprint
import json

from web3 import Web3, exceptions
import gevent
from configurations import GeneralConfig


class BaseABI:

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, chain_id: int, node_url: str, config: object):
        self.chain_id = chain_id
        self._provider = Web3(Web3.HTTPProvider(node_url))
        self.contract_address = config.proxy_address or config.address
        with open(config.abi_path) as f:
            abi = json.load(f)
        self._contract = self._provider.eth.contract(
            address=config.proxy_address or config.address,
            abi=abi
        )

    def balanceOf(self, account: str):
        return self._provider.eth.get_balance(account)

    def transfer(self, address: str, private_key: str, amount: int, recipient: str = None):
        nonce = self._provider.eth.get_transaction_count(address)
        txn = {
            'chainId': self.chain_id,
            'gas': GeneralConfig.GAS_LIMIT,
            'gasPrice': Web3.toWei(GeneralConfig.GAS_PRICE, 'gwei'),
            'to': recipient or self.contract_address,
            'value': amount,
            'nonce': nonce,
        }
        signed_txn = self._provider.eth.account.sign_transaction(txn, private_key=private_key)
        self._provider.eth.send_raw_transaction(signed_txn.rawTransaction)
        txn_hash = Web3.toHex(Web3.keccak(signed_txn.rawTransaction))
        receipt = self._wait_for_transaction(txn_hash)
        pprint.pprint(dict(receipt))
        return receipt

    def _wait_for_transaction(self, txn_hash: str, timeout: float = None):
        with gevent.Timeout(timeout or GeneralConfig.ABI_ACCEPTABLE_WAITING_TIME):
            while True:
                try:
                    txn_receipt = self._provider.eth.get_transaction_receipt(txn_hash)
                    if txn_receipt is not None:
                        break
                except exceptions.TransactionNotFound:
                    print("Waiting for Transaction...")
                gevent.sleep(1)
        return txn_receipt

    def _send_request(self, abi: callable):
        return abi.call()

    def _send_write_request(self, address: str, private_key: str, abi: callable, waiting_time: float = None):
        nonce = self._provider.eth.get_transaction_count(address)
        txn = abi.build_transaction({
            'chainId': self.chain_id,
            'gas': GeneralConfig.GAS_LIMIT,
            'gasPrice': Web3.toWei(GeneralConfig.GAS_PRICE, 'gwei'),
            'from': address,
            'nonce': nonce,
        })
        signed_txn = self._provider.eth.account.sign_transaction(txn, private_key=private_key)
        self._provider.eth.send_raw_transaction(signed_txn.rawTransaction)
        txn_hash = Web3.toHex(Web3.keccak(signed_txn.rawTransaction))
        receipt = self._wait_for_transaction(txn_hash, waiting_time)
        pprint.pprint(dict(receipt))
        return receipt
