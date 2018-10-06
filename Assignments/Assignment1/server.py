from concurrent import futures

import grpc
import time

import chat_pb2_grpc as chat_rpc

from ChatServicer import ChatServicer
from UserServicer import UserServicer


_ONE_DAY_IN_SECONDS = 60 * 60 * 24

def serve():
    port = 50050
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    print('Spartan server started on port {}.'.format(port))   
    chat_rpc.add_ChatServerServicer_to_server(ChatServicer(), server)
    chat_rpc.add_UserServicer_to_server(UserServicer(), server)

    server.add_insecure_port('[::]:' + str(port))
    server.start()
    try:
        while(True):
            time.sleep(_ONE_DAY_IN_SECONDS)
    except(KeyboardInterrupt):
        server.stop(0)
        print('[Spartan] Server Shutdown')

if __name__ == '__main__':
    serve()
