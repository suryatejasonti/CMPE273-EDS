import pickledb
import colorlog
import enum
import logging
import sys

class Message():
    
    def __init__(self, sock, address = None, port = None):
    
        self.port = port
        self.sock = sock
        self.address = (address, self.port)

    def sendMessage(self, message):
        try:
            # Send data
            print ('sending "%s"' % message)
            sent = self.sock.sendto(str.encode(message), self.address)
            return sent
        except Exception as e:
            print ('Sending error {}'.format(e))

    def receiveMessage(self):
        # Receive response
        data, address = self.sock.recvfrom(4096)
        return data.decode()


class PickleDB():

    def __init__(self, port):
        self.db = pickledb.load('assignment3_%s.db' %port, False)

    def setValue(self, key, value):
        val = self.getValue(key)
        if val:
            value = int(val) + int(value)
        self.db.set(key, value)
    
    def getValue(self, key):
        return self.db.get(key)


