import chat_pb2 as chat
import chat_pb2_grpc as chat_rpc

class ChatServicer(chat_rpc.ChatServerServicer):

    def __init__(self):
        # List with all the chat history
        self.chats = []

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
        try:
            # For every client a infinite loop starts (in gRPC's own managed thread)
            while(True):
                # Check if there are any new messages
                while len(self.chats) > lastindex:
                    n = self.chats[lastindex]
                    lastindex += 1
                    yield n
        except KeyboardInterrupt:
            print('i am called')

    def SendMsg(self, request: chat.Message, context):
        """
        This method is called when a clients sends a Note to the server.

        :param request:
        :param context:
        :return:
        """
        print("[{}] {}".format(request.name, request.note))
        # Add it to the chat history
        self.chats.append(request)
        return chat.Empty()
