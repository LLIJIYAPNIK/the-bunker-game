import participant

from app.domain import round


class Game:
    def __init__(
        self, participants: list[participant.Participant], capacity: int
    ):
        self.participants: list[participant.Participant] = participants
        self.capacity: int = capacity

        self.state = None
        self.excluded_players: list[participant.Participant] = []
        self.rounds: list[round.Round] = []

    def start(self): ...

    def finish(self): ...
