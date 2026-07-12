from app.domain import character, user


class Participant:
    def __init__(
        self, user_param: user.User, character_param: character.Character
    ):
        self.user = user_param
        self.character = character_param
