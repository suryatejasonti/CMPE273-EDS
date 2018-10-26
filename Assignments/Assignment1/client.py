'''
client py file to run the client with username
'''
import grpc

import threading
import sys
import atexit

import chat_pb2 as chat
import chat_pb2_grpc as chat_rpc

from crypto import AES_Encrypt

ADDRESS = 'localhost'
PORT = 50050

class Client:

    def __init__(self, u: str):

        self.username = u
        self.userslist = []
        self.encrypt = AES_Encrypt()
        # create a gRPC channel + stub
        with grpc.insecure_channel(ADDRESS + ':' + str(PORT)) as channel:
            
            print('[Spartan] Connected to Spartan Server at port {}.'.format(PORT))

            chat_stub = chat_rpc.ChatServerStub(channel)
            user_stub = chat_rpc.UserStub(channel)
    
            # create new listening thread for when new message streams comes in
            threading.Thread(target=self.receive_message, args=[chat_stub], daemon=True).start()
            self.add_user(chat_stub, user_stub)
            self.chat_options(user_stub, chat_stub)
            self.send_message(chat_stub, user_stub)
    
    def run(self, user_stub, chat_stub):
        for message in chat_stub.ReceiveMsg(chat.Empty()):
            if(message.to == 'client'):
                if(message.method == 'list_users'):
                    

    def message_encrypted(self, to, method, user):
        message = chat.Message()
        message.to = self.encrypt.encrypt(to)
        message.method = self.encrypt.encrypt(method)
        usr = chat.UserData() 
        usr.name = self.encrypt.encrypt(user.name)
        usr.note = self.encrypt.encrypt(user.note)
        chat.Message.user = usr
        message.user = usr
        return message

    def chat_options(self, user_stub, chat_stub):
        self.get_users(chat_stub, user_stub)
        self.single_user_options(user_stub)
        

    def add_user(self, user_stub):
        userdata = chat.UserData()
        userdata.name = self.username
        user_stub.SendMsg(self.message_encrypted('server', 'add_user', userdata))

    def get_users(self, chat_stub, user_stub):
        self.userslist = []
        for _usr in user_stub.GetUsers(chat.Empty()):
            self.userslist.append(self.encrypt.decrypt(_usr.name))
        message = chat.Message()
        message.name = self.encrypt.encrypt('Spartan')
        print_string = 'User list:'
        for usr in self.userslist:
            print_string += '{},'.format(usr)
        message.note = self.encrypt.encrypt(print_string[:-1])
        chat_stub.SendMsg(message)

    def single_user_options(self, user_stub):
        if(len(self.userslist) < 2):
            print('[Spartan] Please wait while other users join to chat')
        else:
            friend = input('[Spartan] Enter a user whom you want to chat with __SPARTAN__: ')
            for usr in self.userslist:
                if friend.strip('__') is usr:
                    print('[Spartan] You are now ready to chat with {}.'.format(friend))                        

    def send_request(self, user_stub):
        print('sending request')

    def receive_message(self, chat_stub):
        '''
        This method will be ran in a separate thread as the main/ui thread, because the for-in call is blocking
        when waiting for new messages
        '''
        for message in chat_stub.ReceiveMsg(chat.Empty()):
            print("[{}] {}".format(self.encrypt.decrypt(message.name), self.encrypt.decrypt(message.note)))

    def send_message(self, chat_stub, user_stub):
        '''
        This method is called when user enters something
        '''
        while(True):
            m = input('[{}]'.format(self.username))
            if m is not '':
                n = chat.Message()
                n.name = self.encrypt.encrypt(self.username)
                n.note = self.encrypt.encrypt(m)
                chat_stub.SendMsg(n)
        
    
    def exit_handler(self, user_stub, chat_stub):
        ur = chat.UserName()
        ur.name = self.encrypt.encrypt(self.username)
        user_stub.RemoveUser(ur)
        print("\n[Spartan] {} exit".format(self.username))
    

        

def main():
    if len(sys.argv) != 2:
        username = input("What's your name?: ")
    else:
        username = sys.argv[1]
    client = Client(username)

def exit_handler(client):
    client.exit_handler()


if __name__ == '__main__':
    main()

#lsof -ti:50050 | xargs kill