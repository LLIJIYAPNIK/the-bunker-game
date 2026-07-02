from app.domain import character, user


class Participant:
    def __init__(self, user_: user.User, character_: character.Character):
        self.user = user_
        self.character = character_

        self.state = None
