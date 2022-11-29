from threading import Lock
import time
from functools import wraps

class Profiler:
    __data = {}
    __lock = Lock()
    __print_always = True

    @classmethod
    def profile(cls, func):
        if not cls.__data.get(func.__name__):
            cls.__data[func.__name__] = {'count': 0, 'time': 0}

        @wraps(func)
        def wrapper(self, *args, **kargs):
            start = time.time()
            func(self, *args, **kargs)
            end = time.time()
            cls.__lock.acquire()
            try:
                cls.__data[func.__name__]['count'] += 1
                cls.__data[func.__name__]['time'] += (end - start)
            finally:
                cls.__lock.release()
            if cls.__print_always:
                print(f'{func.__name__} took {end - start} seconds')
        
        return wrapper

    @classmethod
    def get_avg_runtime(cls, funcname):
        return cls.__data[funcname]['time'] / cls.__data[funcname]['count']