import threading
import sys
from time import sleep

import grpc

import chat_pb2 as chat
import chat_pb2_grpc as chat_rpc
import user_pb2
import user_pb2_grpc

address = 'localhost'
port = 50050
username = ''

class Client:

    def __init__(self, u: str):

        self.username = u
        # create a gRPC channel + stub
        with grpc.insecure_channel(address + ':' + str(port)) as channel:
        
            chat_stub = chat_rpc.ChatServerStub(channel)
            user_stub = user_pb2_grpc.UserStub(channel)
            
            # create new listening thread for when new message streams come in
            threading.Thread(target=self.__listen_for_messages, args=[chat_stub], daemon=True).start()

            self.get_users(user_stub)
            self.send_message(chat_stub)

    def get_users(self, user_stub):
        ur = user_pb2.UserName()
        ur.name = self.username
        print_string = '[Spartan] User list:'
        for usr in user_stub.AddUser(ur):
            print_string += '{},'.format(usr.name)
        print(print_string[:-1])


    def __listen_for_messages(self, chat_stub):
        """
        This method will be ran in a separate thread as the main/ui thread, because the for-in call is blocking
        when waiting for new messages
        """
        for note in chat_stub.ChatStream(chat.Empty()):
            print("\nReceived[{}] {}".format(note.name, note.message))

    def send_message(self, chat_stub):
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
                    chat_stub.SendNote(n)
        except KeyboardInterrupt:
            print("\nBye {}".format(username))
            


if __name__ == '__main__':
    if len(sys.argv) != 2:
        username = input("What's your name?:     ")
    else:
        username = sys.argv[1]
    c = Client(username)