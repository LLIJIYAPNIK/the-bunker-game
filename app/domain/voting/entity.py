from collections import defaultdict

from app.domain import game


class Voting:
    def __init__(self, participants: list[game.Participant]):
        self.participants: list[game.Participant] = participants
        self.statistics = defaultdict(int)

        self.state = None

    def start(self): ...

    def count(self): ...

    def finish(self): ...

    def revote(self, participants: list[game.Participant]): ...
