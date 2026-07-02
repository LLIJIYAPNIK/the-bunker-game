from app.domain.user.entity import User


class Lobby:
    def __init__(self, users: list[User]):
        self.users: list[User] = users

        self.state = None
