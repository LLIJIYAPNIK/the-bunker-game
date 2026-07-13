from app.domain.game import Game, Participant, ParticipantState

from .exceptions import (
    GameIsRunningError,
    GameNotSetError,
    LobbyIsStartedError,
    LobbyNotReadyError,
    NotEnoughPlayersError,
    ParticipantAlreadyInLobbyError,
    ParticipantNotInLobbyError,
)
from .state import LobbyState


class Lobby:
    MIN_PLAYERS = 4

    def __init__(self, participants: list[Participant]):
        self._participants: list[Participant] = participants
        self._game: Game | None = None

        self.state = LobbyState.WAITING

    @property
    def participants(self) -> list[Participant]:
        return self._participants

    @property
    def is_ready(self) -> bool:
        return all(
            p.state == ParticipantState.READY for p in self.participants
        )

    @property
    def ready_participants(self) -> list[Participant]:
        return [
            p for p in self.participants if p.state == ParticipantState.READY
        ]

    @property
    def unready_participants(self) -> list[Participant]:
        return [
            p for p in self.participants if p.state == ParticipantState.UNREADY
        ]

    def add_participant(self, participant: Participant):
        if participant in self.participants:
            raise ParticipantAlreadyInLobbyError()
        self._participants.append(participant)

    def remove_participant(self, participant: Participant):
        if participant not in self.participants:
            raise ParticipantNotInLobbyError()
        self._participants.remove(participant)

    def cast_to_ready(self, participant: Participant):
        if self.state == LobbyState.STARTED:
            raise LobbyIsStartedError()
        participant.ready()
        self._ready_lobby()

    def cast_to_unready(self, participant: Participant):
        if self.state == LobbyState.STARTED:
            raise LobbyIsStartedError()
        participant.unready()
        self.state = LobbyState.WAITING

    def _ready_lobby(self):
        if self.is_ready:
            self.state = LobbyState.READY

    def start_game(self, game: Game):
        if self.state == LobbyState.STARTED:
            raise LobbyIsStartedError()
        if self.state != LobbyState.READY:
            raise LobbyNotReadyError()

        # Official Bunker game rules require a minimum of 4 players
        if len(self.participants) < self.MIN_PLAYERS:
            raise NotEnoughPlayersError()

        self.state = LobbyState.STARTED
        self._game = game
        self._game.start()

    def finish_game(self):
        if self._game is None:
            raise GameNotSetError()
        if self._game.is_running:
            raise GameIsRunningError()
        if self._game.is_finished:
            winners = self._game.winners
            self._game = None
            return winners
        return None
