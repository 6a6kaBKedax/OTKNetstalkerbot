class UserManager:
    def __init__(self):
        self._users = []

    def insertUser(self, user):
        self._users.append(user)

    def searchUser(self, chat_id):
        for user in self._users:
            if(user.chat_id == chat_id):
                return user
        return False