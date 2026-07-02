from app.domain.game_participant.entity import GameParticipant


class Round:
    def __init__(self, participants: list[GameParticipant]):
        self.participant = participants

        self.messages: dict[GameParticipant, str] = {}
        self.voting_result: GameParticipant | None = None
