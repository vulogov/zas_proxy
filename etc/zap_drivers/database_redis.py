__author__  =  'Vladimir Ulogov'
__version__ = 'v0.1.0'

from DatabaseDriver import *
import redis

class DatabaseRedis(DatabaseDriver):
    pass

def main(env, logger, *args, **argv):
    return DatabaseDriverCreator("database_redis", env, logger, DatabaseRedis, args, argv)