from util import Message
import socket
import sys

def main():
    address = 'localhost'
    port = 3000
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    
    messages = ['foo:$10','bar:$30','foo:$20','bar:$20','foo:$30','bar:$10']
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    mess = Message(sock, address, port)

    for message in messages:
        mess.sendMessage(message)
    sock.close()

if __name__ == '__main__':
    main()
