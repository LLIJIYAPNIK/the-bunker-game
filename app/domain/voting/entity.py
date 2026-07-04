from collections import defaultdict
from typing import TypeVar

from .state import VotingState
from .voting_result import VotingResult

T = TypeVar("T")


class Voting[T]:
    def __init__(self, voters: list[T], targets: list[T]):
        self.voted = voters
        self.targets = targets

        self.votes: dict[T, int] = defaultdict(int)

        self.state = VotingState.OPEN

    def start(self):
        self.state = VotingState.OPEN

    def register_vote(self, voter: T, target: T):
        if voter not in self.voted:
            raise ValueError(
                "Voter is already voted or voter is not in voting"
            )
        if target not in self.targets:
            raise ValueError("Target is not in voting")
        if voter == target:
            raise ValueError("Target is same as voter")

        self.voted.remove(voter)
        self.votes[target] += 1

        if not self.voted:
            return self._finish()
        return None

    def _finish(self):
        result = [
            participant
            for participant, vote in self.votes.items()
            if vote == max(self.votes.values())
        ]

        return VotingResult(result)

    def restart(self):
        self.state = VotingState.REVOTE
        current_result = self._finish().winners

        self.voted = self.targets.copy()
        self.targets = current_result.copy()
        self.votes = defaultdict(int)
        self.start()
