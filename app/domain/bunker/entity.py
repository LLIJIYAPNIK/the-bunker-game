from app.domain.game_participant.entity import GameParticipant


class Bunker:
    def __init__(self, capacity):
        self.capacity = capacity

        self.participants: list[GameParticipant] = []
