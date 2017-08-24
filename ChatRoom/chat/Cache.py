class Cache:

    def __init__(self):
        self.users = dict({})
        self.chatrooms = dict({})


class ChatroomCache:

    def __init__(self):
        self.members = None
        self.messages = None
