from app.domain import character


class Participant:
    def __init__(self, user_info: str, character_param: character.Character):
        self.user = user_info
        self.character = character_param
