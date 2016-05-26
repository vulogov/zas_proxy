__author__  =  'Vladimir Ulogov'
__version__ = 'v0.1.0'

import socket

class TCPClient:
    def __init__(self, ip, port, timeout=3):
        self.ip = ip
        self.port = port
        self.timeout = timeout
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setblocking(0)
        self.sock.settimeout(self.timeout)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.connect((self.ip, self.port))
        self.bufsize = 4096
        self.buffer = ''
    def read(self):
        self.buffer = self.sock.recv(self.bufsize)
        return self.buffer
    def write(self, buffer):
        if len(buffer) > self.bufsize:
            raise ValueError, "Buffer too large for TCP socket"
        self.sock.send(buffer)
        self.buffer = buffer
    def close(self):
        self.sock.shutdown()

if __name__ == '__main__':
    c = TCPClient("127.0.0.1", 80)
    c.write('GET /\r\n\r\n')
    print c.read()



