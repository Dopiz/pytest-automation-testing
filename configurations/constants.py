from dataclasses import dataclass


@dataclass
class ContractInfo:
    abi_path: str
    address: str
    proxy_address: str = None


@dataclass
class Database:
    driver: str
    host: str
    port: str
    user: str
    password: str
    database: str
