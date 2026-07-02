from app.domain import game


class Bunker:
    def __init__(self, capacity: int):
        self.capacity = capacity

        self.participants: list[game.Participant] = []

    def add_participant(self, participant: game.Participant): ...
