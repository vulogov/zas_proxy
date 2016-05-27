__version__ = 'v0.1.0'

class DatabaseDriver:
    def  __init__(self, creator):
        self.creator = creator
    def set_db_args(self, args):
        self.args = args


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