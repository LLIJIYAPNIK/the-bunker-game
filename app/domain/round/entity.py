from typing import TypeVar

from app.domain import voting

from .exceptions import (
    VotingInDiscussionRoundError,
    VotingInFinishedRoundError,
)
from .round_result import RoundResult
from .state import RoundState

T = TypeVar("T")


class Round[T]:
    def __init__(self, participants: list[T]):
        self.participant = participants
        self.state = RoundState.DISCUSSION

        self.voters = participants
        self.targets = participants
        self.voting = voting.Voting(self.voters.copy(), self.targets.copy())

    def _finish(self, participant: T):
        self.state = RoundState.FINISHED
        return RoundResult(participant)

    def start_voting(self):
        self.voting.start()
        self.state = RoundState.VOTING

    def _check_states(self):
        if self.state == RoundState.DISCUSSION:
            raise VotingInDiscussionRoundError()
        if self.state == RoundState.FINISHED:
            raise VotingInFinishedRoundError()

    def cast_vote(self, participant: T, target: T):
        self._check_states()

        vote = self.voting.register_vote(participant, target)
        if not isinstance(vote, voting.VotingResult):
            return None
        if vote.needs_revote:
            self._revoting()
            return None
        return self._finish_voting(vote)

    def _finish_voting(self, voting_result: voting.VotingResult):
        return self._finish(voting_result.winners[0])

    def _revoting(self):
        self.voting.restart()
