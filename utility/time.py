import time
from datetime import datetime
from functools import wraps

from dateutil.parser import parse
from dateutil.relativedelta import relativedelta


def wait_until_equals(lambda_func, expected, timeout=15, period=1):
    end_time = time.time() + timeout
    while time.time() < end_time:
        print("Waiting until equals...")
        result = lambda_func()
        if result == expected:
            return True
        time.sleep(period)
    return False


def timeparser(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        arg = tuple()
        for idx in range(len(args)):
            try:
                arg += (parse(args[idx]),)
            except Exception as e:
                # print(f"'{args[idx]}' can't parse to datetime object.")
                arg += (args[idx],)
        for k, v in kwargs.items():
            try:
                kwargs[k] = parse(v)
            except Exception as e:
                # print(f"'{kwargs[k]}' can't parse to datetime object.")
                pass
        return func(*arg, **kwargs)
    return wrapper


class Time:

    @staticmethod
    def now(format=None):
        time = datetime.now()
        if format:
            return time.strftime(format)
        return time

    @staticmethod
    @timeparser
    def timestamp(time=None):
        if not time:
            return datetime.now().timestamp()
        return time.timestamp()

    @staticmethod
    @timeparser
    def formatting(time, format):
        return time.strftime(format)

    @staticmethod
    @timeparser
    def delta(time=None, years=0, months=0, days=0, hours=0, minutes=0, seconds=0, microseconds=0, format=None):
        if not time:
            time = datetime.now()
        time = (
            time
            + relativedelta(
                years=int(years),
                months=int(months),
                days=int(days),
                hours=int(hours),
                minutes=int(minutes),
                seconds=int(seconds),
                microseconds=int(microseconds)
            )
        )
        if format:
            return time.strftime(format)
        return time

    @staticmethod
    @timeparser
    def in_range(time, ref_time, *, years=0, months=0, days=0, hours=0, minutes=0, seconds=0, microseconds=0):
        duration = relativedelta(
            years=int(years),
            months=int(months),
            days=int(days),
            hours=int(hours),
            minutes=int(minutes),
            seconds=int(seconds),
            microseconds=int(microseconds)
        )
        return time - duration <= ref_time <= time + duration

    @staticmethod
    @timeparser
    def is_equal(*times, skip_ms=True):
        compare = list()
        for time in times:
            compare.append(time.timestamp())
        if skip_ms:
            return all(int(time) == int(compare[0]) for time in compare)
        return all(time == compare[0] for time in compare)
