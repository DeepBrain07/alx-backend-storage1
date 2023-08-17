#!/usr/bin/env python3
"""
This is a python module
"""
import redis
from typing import Union, Callable
import uuid
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """ returns a callable """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ class wrapper """
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """ returns a callable """
    func_name = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ class wrapper """
        self._redis.rpush(f'{func_name}:inputs', str(args))
        key = str(uuid.uuid4())
        self._redis.rpush(f'{func_name}:outputs', key)
        if isinstance(key, bytes):
            args = args.decode('utf-8')
        self._redis.set(key, str(args))
        return key
    return wrapper


class Cache:
    """" This is a cache class"""
    def __init__(self):
        """ initializes this class """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ returns a random key """
        key = str(uuid.uuid4())
        if isinstance(key, bytes):
            data = data.decode('utf-8')
        self._redis.set(key, data)
        return key

    @staticmethod
    def get_str(arg: bytes) -> str:
        """ converts the byte object to a string """
        return str(arg)

    @staticmethod
    def get_int(arg: bytes) -> int:
        """ converts the byte object to an int """
        return int(arg)

    def get(self, key: str, fn=None):
        """ converts data(key) back to the required format(fn) """
        value = self._redis.get(key)
        if fn:
            return fn(value)
        return value


def replay(arg) -> None:
    """ This function displays the history
    of calls of a particular function """
    func_name = arg.__qualname__
    i_lst = redis.Redis().lrange("{}:inputs".format(func_name), 0, -1)
    o_lst = redis.Redis().lrange("{}:outputs".format(func_name), 0, -1)
    new = arg(1)

    z_lst = zip(i_lst, o_lst)
    print(f"{func_name} was called {len(o_lst)} times:")
    for name, key in z_lst:
        name = name.decode('utf-8')
        key = key.decode('utf-8')
        print(f"{func_name}(*{name}) -> {key}")
