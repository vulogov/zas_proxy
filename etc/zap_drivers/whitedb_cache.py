__author__  =  'Vladimir Ulogov'
__version__ = 'v0.1.0'

from CacheDriver import *
from CLP import *
from bytes2human import *
import wgdb

class CacheWhitedb(CacheDriver):
    def _open(self, name):
        size = h2b(clp2py(self.args[1]))
        print "DDDDD %s %d"%(name, size)
        self.db = wgdb.attach_database(clp2py(self.args[0]), size)
        self.ready = True
        self.name = name
    def _set(self, key, stamp, value):
        l = wgdb.start_read(self.db)
        q = wgdb.make_query(self.db, arglist=[(0, wgdb.COND_EQUAL, key)])
        rec = wgdb.fetch(self.db, q)
        wgdb.end_read(self.db, l)
        wgdb.free_query(self.db, q)
        l = wgdb.start_write(self.db)
        ## Transaction to Cache
        if not rec:
            rec = wgdb.create_record(self.db, 3)
            wgdb.set_field(self.db, rec, 0, key)
        wgdb.set_field(self.db, rec, 1, stamp)
        wgdb.set_field(self.db, rec, 2, value)
        wgdb.end_write(self.db, l)
    def __get(self, key, field):
        l = wgdb.start_read(self.db)
        rec = wgdb.fetch(self.db, q)
        wgdb.end_read(self.db, l)
        wgdb.free_query(self.db, q)
        if not rec:
            return None
        return wgdb.get_field(self.db, rec, field)
    def _get(self, key):
        return self.__get(key, 2)
    def _age(self, key):
        return self.__get(key, 1)
    def _close(self):
        wgdb.detach_database(self.db)
        self.ready = False
        self.name = ""


class WhiteDBCacheDriverCreator(CacheDriverCreator):
    def init_cache(self):
        for m in self.env.pc.filter(relation="cache_link"):
            drv_name =  clp2py(m.Slots["name"])
            if drv_name != "whitedb_cache":
                continue
            cache_name = clp2py(m.Slots["args"])[0][1]
            drv = self.driver()
            args = []
            for a in m.Slots["args"]:
                args.append(clp2py(a))
            drv.args = tuple(args)
            drv._open(cache_name)
            self.logger.info("Initializing cache %s with size %s bytes"%(cache_name, drv.args[1]))



def main(env, logger, *args, **argv):
    return WhiteDBCacheDriverCreator("whitedb_cache", env, logger, CacheWhitedb, args, argv)