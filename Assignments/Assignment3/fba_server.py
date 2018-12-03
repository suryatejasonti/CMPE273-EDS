import socket
import pickledb
import sys
from util import Message, PickleDB


def main():
    address = 'localhost'
    port = 3000
    if len(sys.argv) > 1:
        port = int(sys.argv[1])

    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((address, port))

    mess = Message(sock, address, port)
    pickle = PickleDB(port)

    while True:
        data = mess.receiveMessage()
        print('Received {}'.format(data))
        key, value = data.split(':$')
        pickle.setValue(key, value)

    sock.close()

if __name__ == '__main__':
    main()
