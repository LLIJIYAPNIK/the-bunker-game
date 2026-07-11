from collections import defaultdict

from .exceptions import (
    TargetDoesNotExistsError,
    VoterAlreadyVotedError,
    VoterSameTargetError,
    VotingClosedError,
)
from .state import VotingState
from .voting_result import VotingResult


class Voting[T]:
    def __init__(self, voters: list[T], targets: list[T]):
        self.voted: dict[T, bool] = {voter: False for voter in voters}

        self.targets = targets

        self.votes: dict[T, int] = defaultdict(int)

        self.state = VotingState.OPEN

    def start(self):
        self.state = VotingState.OPEN

    def register_vote(self, voter: T, target: T):
        if self.state == VotingState.FINISHED:
            raise VotingClosedError()
        if self.voted[voter]:
            raise VoterAlreadyVotedError()
        if target not in self.targets:
            raise TargetDoesNotExistsError()
        if voter == target:
            raise VoterSameTargetError()

        self.state = VotingState.COUNTING

        self.voted[voter] = True
        self.votes[target] += 1

        if all(self.voted.values()):
            return self._finish()
        return None

    def _get_winners(self):
        return [
            participant
            for participant, vote in self.votes.items()
            if vote == max(self.votes.values())
        ]

    def _finish(self):
        self.state = VotingState.FINISHED

        result = self._get_winners()

        return VotingResult(result)

    def restart(self):
        self.state = VotingState.REVOTE
        current_result = self._get_winners()

        voted = self.voted.keys()
        self.voted = {voter: False for voter in voted}
        self.targets = current_result.copy()
        self.votes = defaultdict(int)
