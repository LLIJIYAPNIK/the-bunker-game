from app.domain import bunker, round

from .exceptions import (
    ActiveRoundNotFoundError,
    GameAlreadyStartedError,
    GameNotFinishedError,
    GameNotStartedError,
    ParticipantNotFoundError,
    RoundNotDiscussionError,
)
from .participant import Participant
from .state import GameState


class Game:
    def __init__(self, participants: list[Participant], bunker: bunker.Bunker):
        self.active_participants: list[Participant] = participants
        self.excluded_participants: list[Participant] = []
        self._active_round: round.Round | None = None
        self._rounds: list[round.Round] = []
        self.bunker = bunker

        self.state = GameState.WAITING

    def add_participant(self, participant: Participant):
        if self.state != GameState.WAITING:
            raise GameAlreadyStartedError()
        self.active_participants.append(participant)

    def start(self):
        if self.state != GameState.WAITING:
            raise GameAlreadyStartedError()
        self.state = GameState.RUNNING
        self._start_round()

    def start_round_voting(self):
        if self.active_round.state != round.RoundState.DISCUSSION:
            raise RoundNotDiscussionError()
        self.active_round.start_voting()

    def cast_vote(self, voter: Participant, target: Participant):
        if voter not in self.active_participants:
            raise ParticipantNotFoundError()
        if target not in self.active_participants:
            raise ParticipantNotFoundError()

        res = self.active_round.cast_vote(voter, target)

        if isinstance(res, round.RoundResult):
            self._exclude_participant(res.eliminated)

    def _finish(self):
        if self.state != GameState.RUNNING:
            raise GameNotStartedError()
        self._add_participants_to_bunker(self.active_participants)
        self.state = GameState.FINISHED

    def _start_round(self):
        round_ = round.Round(self.active_participants)
        self._active_round = round_
        self._rounds.append(round_)

    def _exclude_participant(self, participant: Participant):
        self.active_participants.remove(participant)
        self.excluded_participants.append(participant)

        if len(self.active_participants) == self.bunker.profile.capacity:
            self._finish()
        else:
            self._start_round()

    def _add_participants_to_bunker(self, participants: list[Participant]):
        for participant in participants:
            self.bunker.add_participant(participant)

    @property
    def is_running(self):
        return self.state == GameState.RUNNING

    @property
    def is_finished(self):
        return self.state == GameState.FINISHED

    @property
    def participants(self):
        return tuple(self.active_participants)

    @property
    def active_round(self) -> round.Round:
        if self._active_round is None:
            raise ActiveRoundNotFoundError()

        return self._active_round

    @property
    def winners(self):
        if self.state != GameState.FINISHED:
            raise GameNotFinishedError()

        return self.bunker.participants

    @property
    def rounds(self):
        return self._rounds
