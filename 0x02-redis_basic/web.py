#!/usr/bin/env python3
"""
This module defines a 'get page' function
"""
import requests
import redis
from typing import Callable
from functools import wraps


def get_page(url: str) -> str:
    r = redis.Redis()

    def count(f: Callable) -> Callable:
        """ returns a callable """
        @wraps(f)
        def wrapper(*args, **kwargs):
            r.incr(args)
            return f(args)
        return wrapper

    @wraps(count)
    def get(link: str) -> str:
        r.setex(f'count:{url}', 10, str(r.incr(url) - 1))
        return requests.get(link).text

    return get(url)
