__author__  =  'Vladimir Ulogov'
__version__ = 'v0.1.0'

from DatabaseDriver import *
import redis

class DatabaseRedis(DatabaseDriver):
    def _open(self):
        self.r = redis.Redis(host=self.args[0], port=self.args[1])
    def _set(self, key, data):
        self.r.set(key, data)
    def _get(self, key):
        return r.get(key)
    def _keys(self, patt="*"):
        return self.r.keys(pattern=patt)
    def _close(self):
        pass


def main(env, logger, *args, **argv):
    return DatabaseDriverCreator("database_redis", env, logger, DatabaseRedis, args, argv)