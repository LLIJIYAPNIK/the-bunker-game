from collections import defaultdict

from app.domain import game

from .state import VotingState


class Voting:
    def __init__(self, participants: list[game.Participant]):
        self.participants: list[game.Participant] = participants
        self.statistics: dict[game.Participant, int] = defaultdict(int)

        self.state = VotingState.OPEN

        # TODO: Relation with a tie. It should another implementation
        self._result: game.Participant | None = None

    def start(self):
        self.state = VotingState.OPEN

    def cast(self, voter: game.Participant, target: game.Participant):
        # TODO: Add a return value for voting and use it in Round
        # TODO: Add check voter != target
        # TODO: Add check voter and target are active participants
        self.state = VotingState.COUNTING
        self.statistics[target] += 1

    def finish(self):
        result = [
            participant
            for participant, vote in self.statistics.items()
            if vote == max(self.statistics.values())
        ]

        # TODO: Return result here: a tie or a participant, use it in Round()
        if len(result) == 1:
            self.state = VotingState.FINISHED
            self._result = result[0]
        else:
            self._revote(result)

    def _revote(self, participants: list[game.Participant]):
        # TODO: Think about revoting. It should another implementation
        self.state = VotingState.REVOTE
        self.participants = participants
        self.statistics: dict[game.Participant, int] = defaultdict(int)
        self.start()

    def get_result(self) -> game.Participant | None:
        # TODO: finish() has to return result. It should another implementation
        if self.state == VotingState.FINISHED:
            return self._result
        return None
