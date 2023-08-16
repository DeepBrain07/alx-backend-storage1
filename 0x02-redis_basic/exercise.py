#!/usr/bin/env python3
"""
This is a python module
"""
import redis
from typing import Union
import uuid


class Cache:
    """" This is a cache class"""
    def __init__(self):
        """ initializes this class """
        self._redis = redis.Redis()
        self._redis.flushdb()

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
