import socketio

class Starter:
    def __init__(self):
        self.idUser = 1
        self.user = UserAdmin("guest1")

class User:
    def __init__(self, name="player", chatbox=None):
        self.name = name
        self.idUser_of_chatbox = -1
        self.chatbox = chatbox

    @staticmethod
    def update_name():
        return input("New name -->")

    def new_message(self):
        message = input("--> ")
        self.chatbox.send_message(message)
        print()
        self.chatbox.print_chatbox()


class UserAdmin(User):
    def __init__(self, name="player", chatbox=None):
        super().__init__(name, chatbox)
        self.idUser_of_chatbox = 0

    def addUser(self, user, channel):
        if user.idUser_of_chatbox == -1:
            user.idUser_of_chatbox = len(channel.users)
            channel.users.append((user.idUser_of_chatbox, user.name))
        else:
            print("User is already in a", channel.title)

    @staticmethod
    def updateTitle(channel):
        channel.title = input("New title --> ")

class Chatbox:
    def __init__(self, admin_user, title="New chatbox"):
        self.title = title
        self.users = [(0, admin_user.name)]
        self.list_of_messages = []
        self.sio = socketio.Server(cors_allowed_origins='*')

    def printChatbox(self):
        print(f"{self.title} :")
        print()
        print()
        for user, message in zip(self.users, self.list_of_messages):
            print(f"{user[1]} : {message[1]}")
            print()
            print()

    def __str__(self):
        return f"Chatbox('{self.title}', Users: {self.users}, Messages: {self.list_of_messages})"
    
    def send_message(self, message):
        self.list_of_messages.append((0, message))
        self.sio.emit('message', {'user': self.users[0][1], 'content': message})

class Message:
    def __init__(self, author, content):
        self.author = author
        self.content = content