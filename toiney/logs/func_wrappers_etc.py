import random
import logging
import functools
import names

from collections import OrderedDict

from datetime import datetime
from asyncio import sleep
import asyncio
from functools import wraps, partial


# glue code
class event(object):
    def __init__(self, func):
        self.__doc__ = func.__doc__
        self._key = ' ' + func.__name__

    def __get__(self, obj, cls):
        try:
            return obj.__dict__[self._key]
        except KeyError as exc:
            be = obj.__dict__[self._key] = boundevent()
            return be


class boundevent(object):
    def __init__(self):
        self._fns = []

    def __iadd__(self, fn):
        self._fns.append(fn)
        return self

    def __isub__(self, fn):
        self._fns.remove(fn)
        return self

    def __call__(self, *args, **kwargs):
        for f in self._fns[:]:
            f(*args, **kwargs)


def wrap(func):
    @wraps(func)
    async def run(*args, loop=None, executor=None, **kwargs):
        if loop is None:
            loop = asyncio.get_event_loop()
        pfunc = partial(func, *args, **kwargs)
        return await loop.run_in_executor(executor, pfunc)
    return run


def log_func(name="None"):
    now = datetime.now()
    current_time = now.strftime('[%I:%M:%S]')

    logger = logging.getLogger("session")

    if logger.hasHandlers():
        # if logger is already configured, removee all handlers
        logger.handlers = []

    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', current_time)

    # console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    if name == "None":
        # creating file for log
        handler = logging.FileHandler('logs/debug.log')
        handler.setLevel(logging.DEBUG)

        # set log formatter
        handler.setFormatter(formatter)

        # add handler to logging
        logger.addHandler(handler)
    else:
        # creating file(name) for log
        handler = logging.FileHandler('logs/' + str(name))
        handler.setLevel(logging.DEBUG)

        # set log formatter
        handler.setFormatter(formatter)

        # add handler to logging
        logger.addHandler(handler)

    # finally, return logger
    return logger


def log_dbg(f):
        def wrapped(*args, **kwargs):
            """
            wrapper for functions to log func name within function itself
            :param f: function
            :return: function's name
            """
            logger = log_func
            logger().debug("Started '{0}'!".format(f.__name__))
            return f(*args, **kwargs)
        return wrapped


def wait(x, y):
    def decorator(func):
        def wrapper(*args, **kwargs):
            """
            int_1 = integer
            int_2 = integer

            Call this decorator/wrapper with two numbers, like so:
            wait(5, 10)
            """
            rand_num = random.randint(x, y)
            print("Waiting for {0}s before executing...".format(rand_num))
            sleep(rand_num)
            ret = func(*args, **kwargs)
            return ret

        return wrapper

    return decorator


async def wait_alt(x, y):  # alternative function to the above wrapper wait(x, y)
    rand_num = random.randint(x, y)
    print("Waiting for {0}s before executing...".format(rand_num))
    await asyncio.sleep(rand_num)
    return
