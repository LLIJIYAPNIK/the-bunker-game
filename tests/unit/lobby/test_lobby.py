import pytest

from app.domain.game import Game, ParticipantState
from app.domain.lobby import (
    GameIsRunningError,
    GameNotSetError,
    Lobby,
    LobbyIsStartedError,
    LobbyNotReadyError,
    LobbyState,
    NotEnoughPlayersError,
    ParticipantAlreadyInLobbyError,
    ParticipantNotInLobbyError,
)
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


def test_add_participant(lobby):
    p = make_participant("New Player")
    lobby.add_participant(p)
    assert p in lobby.participants
    assert len(lobby.participants) == 4


def test_remove_participant(lobby, players):
    p = players[0]
    lobby.remove_participant(p)
    assert p not in lobby.participants
    assert len(lobby.participants) == 2


def test_lobby_properties(lobby, players):
    players[0].unready()
    assert lobby.is_ready is False
    assert len(lobby.ready_participants) == 2
    assert len(lobby.unready_participants) == 1
    assert players[0] in lobby.unready_participants
    assert players[1] in lobby.ready_participants
    assert players[2] in lobby.ready_participants

    players[0].ready()
    assert lobby.is_ready is True
    assert len(lobby.ready_participants) == 3
    assert len(lobby.unready_participants) == 0


def test_cast_to_ready(lobby, players):
    players[0].unready()
    lobby.state = LobbyState.WAITING
    assert lobby.state == LobbyState.WAITING

    lobby.cast_to_ready(players[0])

    assert players[0].state == ParticipantState.READY
    assert lobby.state == LobbyState.READY


def test_cast_to_unready(lobby, players):
    lobby.state = LobbyState.READY
    lobby.cast_to_unready(players[0])

    assert players[0].state == ParticipantState.UNREADY
    assert lobby.state == LobbyState.WAITING


def test_start_game_raises_not_enough_players_error(lobby):
    lobby.state = LobbyState.READY
    with pytest.raises(NotEnoughPlayersError):
        lobby.start_game(None)


def test_start_game_success(lobby, bunker):
    p4 = make_participant("Player 4")
    lobby.add_participant(p4)
    lobby.state = LobbyState.READY

    game = Game(lobby.participants, bunker)
    lobby.start_game(game)

    assert lobby.state == LobbyState.STARTED
    assert lobby._game is game
    assert game.is_running


def test_finish_game_success(lobby, players, bunker):
    p4 = make_participant("Player 4")
    lobby.add_participant(p4)

    game = Game(lobby.participants, bunker)
    lobby._game = game
    game.start()

    while len(game.active_participants) > game.bunker.profile.capacity:
        game.active_participants.pop()

    game._finish()

    assert game.is_finished

    winners = lobby.finish_game()
    assert lobby._game is None
    assert winners is not None
