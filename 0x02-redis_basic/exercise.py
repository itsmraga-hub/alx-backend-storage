#!/usr/bin/env python3
"""
    Create a Cache class. In the __init__ method, store an instance of the
    Redis client as a private variable named _redis (using redis.Redis())
    and flush the instance using flushdb.
"""
import redis
from typing import Union, Callable, Optional
from functools import wraps
import uuid


def count_calls(method: Callable) -> Callable:
    '''
        Counts the number of times a method is called.
    '''

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        '''
            Wrapper function.
        '''
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """ Decorator to store the history of inputs and
    outputs for a particular function.
    """
    key = method.__qualname__
    inputs = key + ":inputs"
    outputs = key + ":outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):  # sourcery skip:avoid-builtin-shadow
        """ Wrapper for decorator functionality """
        self._redis.rpush(inputs, str(args))
        data = method(self, *args, **kwargs)
        self._redis.rpush(outputs, str(data))
        return data

    return wrapper


def replay(method: Callable) -> None:
    # sourcery skip: use-fstring-for-concatenation,use-fstring-for-formatting
    """
    Replays the history of a function
    Args:
        method: The function to be decorated
    Returns:
        None
    """
    name = method.__qualname__
    cache = redis.Redis()
    calls = cache.get(name).decode("utf-8")
    print("{} was called {} times:".format(name, calls))
    inputs = cache.lrange(name + ":inputs", 0, -1)
    outputs = cache.lrange(name + ":outputs", 0, -1)
    for i, o in zip(inputs, outputs):
        print("{}(*{}) -> {}".format(name, i.decode('utf-8'),
                                     o.decode('utf-8')))


class Cache:
    def __init__(self):
        """
            instance of the redis client
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
            Store method that takes a data argument and returns a string
        """
        key = uuid.uuid4()
        self._redis.set(str(key), data)
        return str(key)

    def get(self, key: str,
            fn: Callable = None) -> Union[str, bytes, int, float, None]:
        """
            takes a key str arg and an optional Callable named fn
        """
        data = self._redis.get(key)
        if data is None or fn is None:
            return None
        return fn(data)

    def get_str(self, key: str) -> Union[str, None]:
        return self.get(key, fn=lambda d: d.decode('utf-8'))

    def get_int(self, key: str) -> Union[int, None]:
        return self.get(key, fn=lambda d: int(d))
