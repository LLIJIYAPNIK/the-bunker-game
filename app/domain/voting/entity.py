from collections import defaultdict

from app.domain.game_participant.entity import GameParticipant


class Voting:
    def __init__(self, participants: list[GameParticipant]):
        self.participants = participants
        self.statistics = defaultdict(int)
