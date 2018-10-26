from functools import lru_cache
from UserServicer import UserServicer
from ratelimiter import rate
from crypto import AES_Encrypt

import chat_pb2 as chat
import chat_pb2_grpc as chat_rpc

class ChatServicer(chat_rpc.ChatServerServicer):

    def __init__(self):
        # List with all the chat history
        self.chats = []
        self.encrypt = AES_Encrypt()
        self.user_stub = UserServicer()

    # The stream which will be used to send new messages to clients
    def ReceiveMsg(self, request_iterator, context):
        """
        This is a response-stream type call. This means the server can keep sending messages
        Every client opens this connection and waits for server to send new messages

        :param request_iterator:
        :param context:
        :return:
        """
        lastindex = 0
        # For every client a infinite loop starts (in gRPC's own managed thread)
        while(True):
            # Check if there are any new messages
            while len(self.chats) > lastindex:
                n = self.chats[lastindex]
                lastindex += 1
                yield n
    def ReceiveMessage(self, request_iterator, context):
        """
        This is a response-stream type call. This means the server can keep sending messages
        Every client opens this connection and waits for server to send new messages

        :param request_iterator:
        :param context:
        :return:
        """
        lastindex = 0
        # For every client a infinite loop starts (in gRPC's own managed thread)
        while(True):
            # Check if there are any new messages
            while len(self.chats) > lastindex:
                n = self.chats[lastindex]
                lastindex += 1
                yield n
    
    def SendMsg(self, request: chat.Message, context):
        """
        This method is called when a clients sends a Note to the server.

        :param request:
        :param context:
        :return:
        """
        print("[{}] {}".format(self.encrypt.decrypt(request.name), self.encrypt.decrypt(request.note)))
        # Add it to the chat history
        self.chats.append(request)
        return chat.Empty()
    
    @rate(15)
    def SendMessage(self, request: chat.Message, context):
        message = self.message_decrypted(request)
        if(self.encrypt.decrypt(message.to) == 'server'):
            if(self.encrypt.decrypt(message.method) == 'add_user'):
                self.user_stub.AddUser(message.user.name)
            elif(self.encrypt.decrypt(message.method) == 'remove_user'):
                self.user_stub.RemoveUser(message.user.name)
            elif(self.encrypt.decrypt(message.method) == 'get_users'):
                self.user_stub.GetUsers()
            print('[{}] {}'.format(message.user.name, message.user.note))
        return chat.Empty()
    
    def message_decrypted(self, message):
        mess = chat.Message()
        mess.to = self.encrypt.decrypt(message.to)
        message.method = self.encrypt.encrypt(message.method)
        usr = chat.UserData() 
        usr.name = self.encrypt.encrypt(message.user.name)
        usr.note = self.encrypt.encrypt(message.user.note)
        message.user = usr
        return mess