from app.domain.character.entity import Character
from app.domain.user.entity import User


class GameParticipant:
    def __init__(self, user: User, character: Character):
        self.user = user
        self.character = character

        self.state = None
