__author__  =  'Vladimir Ulogov'
__version__ = 'v0.1.0'

########################################################################################################################
## Service fuctions
########################################################################################################################
def check_file(fname, mode):
    fname = os.path.expandvars(fname)
    if os.path.exists(fname) and os.path.isfile(fname) and os.access(fname, mode):
        return True
    return False

def check_directory(dname):
    dname = os.path.expandvars(dname)
    if os.path.exists(dname) and os.path.isdir(dname) and os.access(dname, os.R_OK):
        return True
    return False

def check_file_read(fname):
    return check_file(fname, os.R_OK)

def Is_Process_Running():
    global ARGS, logger

    try:
        pid = int(open(ARGS.pid).read())
    except:
        logger.error("Can not detect ZAP process ID from %s" % ARGS.pid)
        return None
    if not os.path.exists('/proc/%d' % pid):
        logger.info("ZAP process with PID=%d isn't running. Removing stale PID file" % pid)
        os.unlink(args.pid)
        return None
    return pid

def check_module(fname):
    if not check_file_read(fname):
        return False
    if os.path.getsize(fname) > 0:
        return True
    return False

def check_file_write(fname):
    return check_file(fname, os.W_OK)

def check_file_exec(fname):
    return check_file(fname, os.X_OK)

def get_dir_content(dname):
    if not check_directory(dname):
        return []
    ret = []
    for f in os.listdir(dname):
        if not check_file_read("%s/%s"%(dname, f)):
            continue
        ret.append((f, "%s/%s"%(dname, f), os.path.splitext(f)))
    return ret

def rchop(thestring, ending):
  if thestring.endswith(ending):
    return thestring[:-len(ending)]
  return thestring


class Object(object):
    def Object__set_attr(self, key, argv, default=None):
        if argv.has_key(key):
            setattr(self, key, argv[key])
        else:
            setattr(self, key, default)
    def Initialize(self):
        import inspect
        for c in inspect.getmro(self.__class__):
            try:
                init_method = getattr(c, "Init")
            except AttributeError:
                continue
            apply(init_method, (self,))

