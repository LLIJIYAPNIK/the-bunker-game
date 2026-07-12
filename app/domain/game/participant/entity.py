from app.domain import character, user

from .state import ParticipantState


class Participant:
    def __init__(
        self, user_param: user.User, character_param: character.Character
    ):
        self.user = user_param
        self.character = character_param

        self.state = ParticipantState.ACTIVE
