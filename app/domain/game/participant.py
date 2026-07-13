from app.domain import character

from .state import ParticipantState


class Participant:
    def __init__(self, user_info: str, character_param: character.Character):
        self.user = user_info
        self.character = character_param
        self.state = ParticipantState.READY

    def ready(self):
        self.state = ParticipantState.READY

    def unready(self):
        self.state = ParticipantState.UNREADY
