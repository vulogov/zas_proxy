__author__  =  'Vladimir Ulogov'
__version__ = 'v0.1.0'

import socket

class TCPClient:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.ip, self.port))

