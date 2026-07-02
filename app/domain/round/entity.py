from app.domain import game


class Round:
    def __init__(self, participants: list[game.Participant]):
        self.participant = participants

        self.messages: dict[game.Participant, str] = {}
        self.voting_result: game.Participant | None = None

    def start(self): ...

    def finish(self): ...

    def participant_say(self, participant: game.Participant, phrase: str): ...

    def start_voting(self): ...

    def finish_voting(self): ...
