from app.domain.game_participant.entity import GameParticipant


class Game:
    def __init__(self, participants: list[GameParticipant], capacity: int):
        self.participants: list[GameParticipant] = participants
        self.capacity: int = capacity

        self.state = None
        self.excluded_players: list[GameParticipant] = []
