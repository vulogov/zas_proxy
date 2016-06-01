__author__  =  'Vladimir Ulogov'
__version__ = 'v0.1.0'

from Object import Object

def clp2py(val):
    try:
        t,v = val.clrepr()
    except:
        return val
    if t in [0,1,3]:
        return v
    elif t == 2 and v == 'TRUE':
        return True
    elif t == 2 and v == 'FALSE':
        return False
    return v

def multifield2py(val):
    out = []
    for f in val:
        out.append(clp2py(f))
    return tuple(out)

class FACT:
    def facts(self, fname):
        self.clips.LoadFacts(fname)
    def load_facts(self, **args):
        return self._load(self.clips.LoadFacts, self.clips.LoadFactsFromString, args)

class LOADER:
    def _load(self, lf_file, lf_string, args):
        if args.has_key("file") and lf_file:
            if not check_module(args["file"]):
                raise IOError, "File %s not found or not accessible"%args["file"]
            return apply(lf_file, (args["file"],))
        elif args.has_key("data") and len(args["data"]) and lf_string:
            return apply(lf_string, (args["data"],))
        else:
            raise ValueError, "Loader requested to load not from file, nether from string"

class CLPEXEC:
    def load(self, **args):
        return self._load(self.clips.Load, self.clips.Eval, args)
    def execute(self, **args):
        return self._load(self.clips.BatchStar, self.clips.Eval, args)

class CLP(Object, LOADER, FACT, CLPEXEC):
    def __init__(self, **argv):
        self.argv = argv
        self.clips = clips.Environment()
        self.clear()
    def clear(self):
        self.clips.Clear()
        self.clips.Reset()
    def current(self):
        self.clips.SetCurrent()