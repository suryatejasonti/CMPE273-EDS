class UserServicer():

    def __init__(self):
        # List with all the users history
        self.users = []

    def AddUser(self, username):
        # Add user to users list
        self.users.append(username)

    def RemoveUser(self, username):
        #Remove user from users list
        self.users.remove(username)

    def GetUsers(self):
        # For every client a infinite loop starts (in gRPC's own managed thread)
        for user in self.users:
            yield user

    