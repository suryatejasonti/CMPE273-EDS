from concurrent import futures

import grpc
import time

import chat_pb2 as chat
import chat_pb2_grpc as chat_rpc
import user_pb2
import user_pb2_grpc


_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class ChatServicer(chat_rpc.ChatServerServicer):

    def __init__(self):
        # List with all the chat history
        self.chats = []

    # The stream which will be used to send new messages to clients
    def ChatStream(self, request_iterator, context):
        """
        This is a response-stream type call. This means the server can keep sending messages
        Every client opens this connection and waits for server to send new messages

        :param request_iterator:
        :param context:
        :return:
        """
        lastindex = 0
        # For every client a infinite loop starts (in gRPC's own managed thread)
        while True:
            # Check if there are any new messages
            while len(self.chats) > lastindex:
                n = self.chats[lastindex]
                lastindex += 1
                yield n

    def SendNote(self, request: chat.Note, context):
        """
        This method is called when a clients sends a Note to the server.

        :param request:
        :param context:
        :return:
        """
        print("[{}] {}".format(request.name, request.message))
        # Add it to the chat history
        self.chats.append(request)
        return chat.Empty()

class UserServicer(user_pb2_grpc.UserServicer):

    def __init__(self):
        # List with all the users history
        self.users = []

    def AddUser(self, request: user_pb2.UserName, context):
        self.users.append(request)
        lastindex = 0
        # For every client a infinite loop starts (in gRPC's own managed thread)
        # Check if there are any new messages
        while len(self.users) > lastindex:
            n = self.users[lastindex]
            lastindex += 1
            yield n

    def RemoveUser(self, request: user_pb2.UserName, context):
        lastindex = 0
        # Check if there are any new messages
        while len(self.users) > lastindex:
            n = self.users[lastindex]
            lastindex += 1
            yield n

def serve():
    port = 50050
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    chat_rpc.add_ChatServerServicer_to_server(ChatServicer(), server)
    user_pb2_grpc.add_UserServicer_to_server(UserServicer(), server)

    print('Starting server. Listening...')
    server.add_insecure_port('[::]:' + str(port))
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)
    finally:
        server.stop(0)

if __name__ == '__main__':
    serve()
