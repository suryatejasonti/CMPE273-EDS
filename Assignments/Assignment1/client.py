'''
client py file to run the client with username
'''
import threading
import sys
import grpc

import chat_pb2 as chat
import chat_pb2_grpc as chat_rpc

from crypto import AESEncrypt

ADDRESS = 'localhost'
PORT = 50050

class Client:

    def __init__(self, u: str):

        self.username = u
        self.userslist = []
        self.encrypt = AESEncrypt()
        # create a gRPC channel + stub
        with grpc.insecure_channel(ADDRESS + ':' + str(PORT)) as channel:
            
            print('[Spartan] Connected to Spartan Server at port {}.'.format(PORT))

            chat_stub = chat_rpc.ChatServerStub(channel)
            user_stub = chat_rpc.UserStub(channel)
            
            self.add_user(chat_stub, user_stub)            
            # create new listening thread for when new message streams comes in
            threading.Thread(target=self.__listen_for_messages, args=[chat_stub], daemon=True).start()

            self.send_request(user_stub)
            self.send_message(chat_stub, user_stub)

    def add_user(self, chat_stub, user_stub):
        ur = chat.UserName()
        ur.name = self.username
        user_stub.AddUser(ur)
        self.__get_users(chat_stub, user_stub)

    def __get_users(self, chat_stub, user_stub):
        self.userslist = []
        for usr in user_stub.GetUsers(chat.Empty()):
            self.userslist.append(usr)
        message = chat.Message()
        message.name = 'Spartan'
        print_string = 'User list:'
        for usr in self.userslist:
            print_string += '{},'.format(usr.name)
        message.note = print_string[:-1]
        chat_stub.SendMsg(message)

    def send_request(self, user_stub):
        if(len(self.userslist) < 2):
            print('[Spartan] Please wait while other users join to chat')
        else:    
            friend = input('[Spartan] Enter a user whom you want to chat with __SPARTAN__: ')
            for usr in self.userslist:
                if friend.strip('__') is usr.name:
                    print('[Spartan] You are now ready to chat with {}.'.format(friend))

    def __listen_for_messages(self, chat_stub):
        '''
        This method will be ran in a separate thread as the main/ui thread, because the for-in call is blocking
        when waiting for new messages
        '''
        for message in chat_stub.ReceiveMsg(chat.Empty()):
            decrypted_message = self.encrypt.decrypt(message)
            print("[{}] {}".format(decrypted_message.name, decrypted_message.note))


    def send_message(self, chat_stub, user_stub):
        '''
        This method is called when user enters something
        '''
        try:
            while(True):
                m = input('[{}]'.format(self.username))
                #print('[{}]'.format(USERNAME))
                if m is not '':
                    n = chat.Message()
                    n.name = self.username
                    n.note = m
                    chat_stub.SendMsg(self.encrypt.encrypt(n), timeout = 4)
        except KeyboardInterrupt:
            ur = chat.UserName()
            ur.name = self.username
            user_stub.RemoveUser(ur)
            print("\n[Spartan] {} exit".format(self.username))


def main():
    if len(sys.argv) != 2:
        username = input("What's your name?: ")
    else:
        username = sys.argv[1]
    Client(username)


if __name__ == '__main__':
    main()

#lsof -ti:50050 | xargs kill