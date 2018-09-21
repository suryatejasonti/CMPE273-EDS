import threading
import sys
from time import sleep

import grpc

import chat_pb2 as chat
import chat_pb2_grpc as rpc

address = 'localhost'
port = 50050
username = ''

class Client:

    def __init__(self, u: str):

        self.username = u
        # create a gRPC channel + stub
        channel = grpc.insecure_channel(address + ':' + str(port))
        self.conn = rpc.ChatServerStub(channel)
        # create new listening thread for when new message streams come in
        threading.Thread(target=self.__listen_for_messages, daemon=True).start()
        self.send_message()

    def __listen_for_messages(self):
        """
        This method will be ran in a separate thread as the main/ui thread, because the for-in call is blocking
        when waiting for new messages
        """
        for note in self.conn.ChatStream(chat.Empty()):
            print("\nReceived[{}] {}".format(note.name, note.message))

    def send_message(self):
        """
        This method is called when user enters something
        """
        try:
            while True:
                m = input("\nSay something:   ")
                if m is not '':
                    n = chat.Note()
                    n.name = self.username
                    n.message = m
                    print("\nSent[{}] {}".format(self.username, m))
                    self.conn.SendNote(n)
        except KeyboardInterrupt:
            print("\nBye {}".format(username))
            


if __name__ == '__main__':
    if len(sys.argv) != 2:
        username = input("What's your name?:     ")
    else:
        username = sys.argv[1]
    c = Client(username)