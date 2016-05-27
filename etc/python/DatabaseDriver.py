__version__ = 'v0.1.0'

class DatabaseDriver:
    def  __init__(self, creator):
        self.creator = creator
        self.ready = False
    def set_db_args(self, args):
        self.args = args
    def open(self):
        self._open()
        self.ready = True
    def set(self, key, src="", **data):
        if not self.ready:
            self.open()
        _key = "%s:%s"%(src, key)
        self._set(_key, data)
    def set_value(self, key, src, d):
        if not self.ready:
            self.open()
        _key = "%s:%s"%(src, key)
        self._set(_key, d)
    def get(self, key, src=""):
        if not self.ready:
            self.open()
        _key = "%s:%s" % (src, key)
        return self._get(_key)
    def keys(self, src="", patt="*"):
        if not self.ready:
            self.open()
        _patt = "%s:%s"%(src, patt)
        return self._keys(_patt)
    def close(self):
        if not self.ready:
            self.open()
        self._close()


class DatabaseDriverCreator:
    def __init__(self, name, env, logger, cls, args, argv):
        self.cls = cls
        self.name = name
        self.env = env
        self.logger = logger
        self.args = args
        self.argv = argv
    def driver(self):
        return self.cls(self)