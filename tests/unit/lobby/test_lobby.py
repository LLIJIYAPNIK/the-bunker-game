import pytest

from app.domain.game import Game
from app.domain.lobby.entity import Lobby
from app.domain.lobby.exceptions import (
    GameIsRunningError,
    GameNotSetError,
    LobbyIsStartedError,
    LobbyNotReadyError,
    ParticipantAlreadyInLobbyError,
    ParticipantNotInLobbyError,
)
from app.domain.lobby.state import LobbyState
from tests.factories.participant import make_participant


@pytest.fixture
def lobby(players):
    return Lobby(players)


def test_add_participant_raises_participant_already_in_lobby_error(
    lobby, players
):
    with pytest.raises(ParticipantAlreadyInLobbyError):
        lobby.add_participant(players[0])


def test_remove_participant_raises_participant_not_in_lobby_error(lobby):
    p = make_participant("4")
    with pytest.raises(ParticipantNotInLobbyError):
        lobby.remove_participant(p)


def test_cast_to_ready_raises_lobby_is_started_error(lobby, players):
    lobby.state = LobbyState.STARTED
    with pytest.raises(LobbyIsStartedError):
        lobby.cast_to_ready(players[0])


def test_cast_to_unready_raises_lobby_is_started_error(lobby, players):
    lobby.state = LobbyState.STARTED
    with pytest.raises(LobbyIsStartedError):
        lobby.cast_to_unready(players[0])


def test_start_game_raises_lobby_not_ready_error_when_waiting(lobby):
    lobby.state = LobbyState.WAITING
    with pytest.raises(LobbyNotReadyError):
        lobby.start_game(None)


def test_start_game_raises_lobby_not_ready_error_when_not_ready(lobby):
    lobby.state = LobbyState.CLOSED
    with pytest.raises(LobbyNotReadyError):
        lobby.start_game(None)


def test_start_game_raises_lobby_is_started_error_when_started(lobby):
    lobby.state = LobbyState.STARTED
    with pytest.raises(LobbyIsStartedError):
        lobby.start_game(None)


def test_finish_game_raises_game_not_set_error(lobby):
    with pytest.raises(GameNotSetError):
        lobby.finish_game()


def test_finish_game_raises_game_is_running_error(lobby, players, bunker):
    game = Game(players, bunker)
    game.start()
    lobby._game = game
    with pytest.raises(GameIsRunningError):
        lobby.finish_game()
