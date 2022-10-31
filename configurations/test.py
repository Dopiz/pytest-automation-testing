from . import defaults
from .constants import ContractInfo, Database

    
class GeneralConfig(defaults.GeneralConfig):
    ENV = "test"
    BSC_CHAIN_ID = 97
    BSC_NODE_URL = "https://data-seed-prebsc-1-s1.binance.org:8545"
    

class GamefiConfig(defaults.GamefiConfig):
    BASE_URL = "http://localhost:8787"
    RACE_CONTRACT = ContractInfo(
        abi_path="abi/gamefi/race_abi.json",
        address="0xfbd411e2a123456787057357faab89e790240b34",
        proxy_address="0xAfa12345678808B068f31CfB638161377Cc4920D"
    )
    NFT_CONTRACT = ContractInfo(
        abi_path="abi/gamefi/vehicle_nft_abi.json",
        address="0xacacad7591a123456782689187c4784112156405",
        proxy_address="0xec65E12345678C9e54B1B2f1a5107061683A2B3d"
    )
    DATABASE = Database(
        driver="mysql",
        host="https://localhost",
        port="443",
        user="user",
        password="password",
        database="gamefi"
    )
    
