__author__  =  'Vladimir Ulogov'
__version__ = 'v0.1.0'

import copy

def build_chain(d, node, c_list=[]):
    if d.has_key(node):
        for cn in d[node]:
            c_list.append(cn)
            c_list = build_chain(d, cn, c_list)
    return c_list

class ProtocolDriver:
    def __init__(self, creator):
        self.creator = creator
        self.name = creator.name
        self.env = self.creator.env
        self.logger = self.creator.logger
        self.args = self.creator.args
        self.argv = self.creator.argv
    def build_chain(self):
        self.chain = build_chain(self.env.drv.chain, self.name)
        self.rcv_drivers = []
        self.send_drivers = []
        for d in self.chain[::-1]:
            _d = self.env.drv.driver(d).driver()
            _d.set_drv_context(self.ctx)
            self.rcv_drivers.append(_d)
        for d in self.chain:
            _d = self.env.drv.driver(d).driver()
            _d.set_drv_context(self.ctx)
            self.send_drivers.append(_d)
    def update_ctx_in_chain(self, **ctx):
        for d in self.rcv_drivers:
            for k in ctx.keys():
                d.ctx[k] = ctx[k]
        for d in self.send_drivers:
            for k in ctx.keys():
                d.ctx[k] = ctx[k]


    def set_drv_context(self, _ctx={}, **ctx):
        self.ctx = _ctx
        for k in ctx.keys():
            self.ctx[k] = ctx[k]

    def recv_data(self, data):
        return data

    def recv(self, sock, buf_len=1024):
        buf = ""
        while True:
            _buf = self._recv(sock, buf_len)
            if not buf or len(buf) == 0:
                break
            buf += _buf
        data = buf
        for d in self.rcv_drivers:
            data = d.recv_data(data)
        return self.recv_data(data)

    def _recv(self, sock, buf_len=1024):
        buf = sock.recv(buf_len)
        return buf

    def send_data(self, data):
        return data

    def send(self, sock, data):
        data = self.send_data(data)
        for d in self.send_drivers:
            data = d.send_data(data)
        sock.send(data)
    def toChain(self, data):
        _data = self.send_data(data)
        print data,type(data)
        for d in self.send_drivers:
            print d.name,_data,type(_data)
            _data = d.send_data(_data)
        return _data
    def fromChain(self, data):
        _data = data
        for d in self.rcv_drivers:
            _data = d.recv_data(_data)
        return self.recv_data(_data)




class ProtocolDriverCreator:
    def __init__(self, name, env, logger, cls, args, argv):
        self.cls = cls
        self.name = name
        self.env = env
        self.logger = logger
        self.args = args
        self.argv = argv
    def driver(self):
        return self.cls(self)

