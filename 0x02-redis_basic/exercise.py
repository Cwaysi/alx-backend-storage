#!/usr/bin/env python3
"""
Redis module, Writing 
"""
import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Prototype: def count_calls
    """
    @wraps(method)
    def wrapper(self, *args, **kwds):
        """
        Prototype: def wrapper
        """
        skey_m = method.__qualname__
        self._redis.incr(skey_m)
        return method(self, *args, **kwds)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
       Returns a Callable
    """
    @wraps(method)
    def wrapper(self, *args, **kwds):
        """
        ......redis
        """
        skey_m = method.__qualname__
        sinp_m = skey_m + ':inputs'
        soutp_m = skey_m + ":outputs"
        data = str(args)
        self._redis.rpush(sinp_m, data)
        finee = method(self, *args, **kwds)
        self._redis.rpush(soutp_m, str(finee))
        return finee
    return wrapper


def replay(func: Callable):
    """
        Displays history of calls of a particular function
    """
    r = redis.Redis()
    skey_m = func.__qualname__
    sinp_m = r.lrange("{}:inputs".format(skey_m), 0, -1)
    soutp_m = r.lrange("{}:outputs".format(skey_m), 0, -1)
    calls_number = len(sinp_m)
    times_str = 'times'
    if calls_number == 1:
        times_str = 'time'
    fin = '{} was called {} {}:'.format(skey_m, calls_number, times_str)
    print(fin)
    for k, v in zip(sinp_m, soutp_m):
        fin = '{}(*{}) -> {}'.format(
            skey_m, k.decode('utf-8'), v.decode('utf-8'))
        print(fin)


class Cache():
    """
    Store instanc
    """
    def __init__(self):
        """
        Prototype: d Redis client as private variable _redis
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store histor a particular function
        """
        gen = str(uuid.uuid4())
        self._redis.set(gen, data)
        return gen

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """
        Convert d desired format
        """
        val = self._redis.get(key)
        return val if not fn else fn(val)

    def get_int(self, key):
        return self.get(key, int)

    def get_str(self, key):
        value = self._redis.get(key)
        return value.decode("utf-8")
