import decimal
from decimal import Decimal

EMPTY_STRING = ""
FALSE_STRING = "false"


def round(number, digits=0):
    decimal.getcontext().rounding = "ROUND_HALF_UP"
    number = decimal.Decimal(str(number), decimal.getcontext())
    return Decimal(number).__round__(digits)


def to_bool(string):
    if (string is not None
        and string != EMPTY_STRING
        and str(string).lower() != FALSE_STRING
            and to_int(string) != 0):
        return True
    return False


def to_int(string):
    try:
        return int(Decimal(string))
    except (ValueError, Exception) as e:
        return string


def to_decimal(string):
    try:
        return Decimal(string)
    except (ValueError, Exception) as e:
        return string


def to_float(string):
    try:
        return float(string)
    except (ValueError, Exception) as e:
        return string


def percent_to_string(percent: float):
    if percent % 1:
        return f"{int(percent * 100)}%"
    return f"{percent * 100}%"


def scale_from_wei(number):
    decimal.getcontext().prec = 17
    return Decimal(number) / Decimal(1e18)


def scale_to_wei(number):
    decimal.getcontext().prec = 17
    return Decimal(number) * Decimal(1e18)


def scale_from_kwei(number):
    decimal.getcontext().prec = 14
    return Decimal(number) / Decimal(1e15)


def scale_to_kwei(number):
    decimal.getcontext().prec = 14
    return Decimal(number) * Decimal(1e15)


def scale_from_mwei(number):
    decimal.getcontext().prec = 11
    return Decimal(number) / Decimal(1e12)


def scale_to_mwei(number):
    decimal.getcontext().prec = 11
    return Decimal(number) * Decimal(1e12)


def scale_from_gwei(number):
    decimal.getcontext().prec = 8
    return Decimal(number) / Decimal(1e9)


def scale_to_gwei(number):
    decimal.getcontext().prec = 8
    return Decimal(number) * Decimal(1e9)
