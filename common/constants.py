from enum import Enum, IntEnum, unique


@unique
class ContractRespStatus(IntEnum):
    SUCCESS = 1


@unique
class APIRespStatus(str, Enum):
    SUCCESS = "0000"
    SYSTEM_ABNORMALITY = "9999"
