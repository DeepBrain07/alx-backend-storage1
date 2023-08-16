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
        self._redis.flushdb

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ returns a random key """
        key = str(uuid.uuid4())
        if type(data) == bytes:
            data = data.decode('utf-8')
        self._redis.set(key, data)
        return key
