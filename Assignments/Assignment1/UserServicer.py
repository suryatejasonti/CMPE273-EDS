import chat_pb2 as chat
import chat_pb2_grpc as chat_rpc

class UserServicer(chat_rpc.UserServicer):

    def __init__(self):
        # List with all the users history
        self.users = []
        self.group = chat.Group
        self.lastindex = 0
        self.newuseradded = False

    def AddUser(self, request: chat.UserName, context):
        # Add user to users list
        self.users.append(request)
        self.newuseradded = True
        return chat.Empty()

    def RemoveUser(self, request: chat.UserName, context):
        #Remove user from users list
        self.users.remove(request)
        return chat.Empty()

    def GetUsers(self, request_iterator, context):
        # For every client a infinite loop starts (in gRPC's own managed thread)
        if self.newuseradded:
            for usr in self.users:
                yield usr
                self.newuseradded = False
        
            
    def FriendRequest(self, request: chat.Group, context):
        #send friend request
        self.group = request 
