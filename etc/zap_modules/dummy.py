__author__  =  'Vladimir Ulogov'
__version__ = 'v0.1.0'

def main(env, logger, *args, **argv):
    args = tuple(list(args[2:]))
    logger.info("This startup function doesn't do much %s %s"%(repr(env),repr(args)))
