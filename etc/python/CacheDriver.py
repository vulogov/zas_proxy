__version__ = 'v0.1.0'

import time

class CacheDriver:
    def  __init__(self, creator):
        self.creator = creator
        self.ready = False
        self.name = ""
    def set_cache_args(self, args):
        self.args = args
    def set(self, name, key, value):
        if not self.ready or self.name != name:
            self._open(name)
            if not self.ready:
                return False
        self._set(key, time.time(), value)
    def get(self, name, key):
        if not self.ready or self.name != name:
            self._open(name)
            if not self.ready:
                raise KeyError, key
        return self._get(key)
    def age(self, name, key):
        if not self.ready or self.name != name:
            self._open(name)
            if not self.ready:
                raise KeyError, key
        return self._age(key)
    def acquire(self, name, key):
        self.set(name, "lock:%s"%key, 1)
    def release(self, name, key):
        self.set(name, "lock:%s"%key, 0)
    def lock(self, name, key):
        res = self.get("lock:%s"%name, key)
        if res == None or res == 0:
            return False
        return True
    def close(self):
        if not self.ready:
            return
        self._close()




class CacheDriverCreator:
    def __init__(self, name, env, logger, cls, args, argv):
        self.cls = cls
        self.name = name
        self.env = env
        self.logger = logger
        self.args = args
        self.argv = argv
        self.init_cache()
    def init_cache(self):
        pass
    def driver(self):
        return self.cls(self)