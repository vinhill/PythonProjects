from threading import Lock
import time

class Profiler:
    __data = {}
    __lock = Lock()

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
        
        return wrapper

    @classmethod
    def get_avg_runtime(cls, funcname):
        return cls.__data[funcname]['time'] / cls.__data[funcname]['count']