from app.domain import game, voting
from app.domain.voting.voting_result import VotingResult

from .round_result import RoundResult
from .state import RoundState


class Round:
    def __init__(self, participants: list[game.Participant]):
        self.participant = participants
        self.state = RoundState.DISCUSSION

        self.voters = participants
        self.targets = participants
        self.voting = voting.Voting(self.voters.copy(), self.targets.copy())

    def _finish(self, participant: game.Participant):
        self.state = RoundState.FINISHED
        return RoundResult(participant)

    def start_voting(self):
        self.voting.start()
        self.state = RoundState.VOTING

    def cast_vote(
        self, participant: game.Participant, target: game.Participant
    ):
        vote = self.voting.register_vote(participant, target)
        if not isinstance(vote, VotingResult):
            return None
        if vote.needs_revote:
            self._revoting()
            return None
        return self._finish_voting(vote)

    def _finish_voting(self, voting_result: VotingResult):
        return self._finish(voting_result.winners[0])

    def _revoting(self):
        self.voting.restart()
