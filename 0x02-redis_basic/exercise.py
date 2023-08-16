#!/usr/bin/env python3
"""
    Create a Cache class. In the __init__ method, store an instance of the Redis
    client as a private variable named _redis (using redis.Redis()) and
    flush the instance using flushdb.
"""
import redis
from typing import Union
import uuid


class Cache:
    def __init__(self):
        """
            instance of the redis client
        """
        self._redis = redis.Redis()
        self._redis.flushdb()


    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
            Store method that takes a data argument and returns a string
        """

        key = uuid.uuid4()
        self._redis.set(str(key), data)
        return str(key)

