import pytest

from app.domain.bunker import (
    Bunker,
    BunkerProfile,
    Catastrophe,
    TimeToOutYears,
)
from app.domain.game import (
    ActiveRoundNotFoundError,
    Game,
    GameAlreadyStartedError,
    GameNotFinishedError,
    GameNotStartedError,
    Participant,
    ParticipantNotFoundError,
    RoundNotDiscussionError,
)
from app.domain.game.state import GameState


@pytest.fixture
def game_bunker() -> Bunker[Participant]:
    profile = BunkerProfile(
        catastrophe=Catastrophe(
            name="Virus",
            description="Deadly virus",
            preferred_professions=set(),
            preferred_items=set(),
        ),
        conditions=(),
        time_to_out_years=TimeToOutYears(
            years=10,
            preferred_max_age=40,
        ),
        capacity=1,
    )
    return Bunker(profile)


@pytest.fixture
def game(players: list[Participant], game_bunker: Bunker[Participant]) -> Game:
    return Game(players.copy(), game_bunker)


def test_game_initial_state(game: Game, players: list[Participant]):
    assert game.state == GameState.WAITING
    assert not game.is_running
    assert not game.is_finished
    assert game.participants == tuple(players)
    assert game.rounds == []

    with pytest.raises(ActiveRoundNotFoundError):
        _ = game.active_round

    with pytest.raises(GameNotFinishedError):
        _ = game.winners


def test_add_participant(game: Game, player: Participant):
    new_player = player
    game.add_participant(new_player)

    assert new_player in game.participants
    assert len(game.participants) == 4


def test_start_game(game: Game, players: list[Participant]):
    game.start()

    assert game.state == GameState.RUNNING
    assert game.is_running
    assert not game.is_finished
    assert len(game.rounds) == 1

    round_ = game.active_round
    assert round_.participant == players


def test_start_game_already_started(game: Game):
    game.start()

    with pytest.raises(GameAlreadyStartedError):
        game.start()


def test_add_participant_after_start_raises(game: Game, player: Participant):
    game.start()

    with pytest.raises(GameAlreadyStartedError):
        game.add_participant(player)


def test_start_round_voting(game: Game):
    game.start()
    game.start_round_voting()

    assert game.active_round.state.name == "VOTING"


def test_start_round_voting_not_discussion(game: Game):
    game.start()
    game.start_round_voting()

    with pytest.raises(RoundNotDiscussionError):
        game.start_round_voting()


def test_cast_vote(game: Game, players: list[Participant]):
    game.start()
    game.start_round_voting()

    p1, p2, p3 = players

    game.cast_vote(p1, p2)
    assert len(game.excluded_participants) == 0


def test_cast_vote_voter_not_found(
    game: Game, players: list[Participant], player: Participant
):
    game.start()
    game.start_round_voting()

    with pytest.raises(ParticipantNotFoundError):
        game.cast_vote(player, players[0])


def test_cast_vote_target_not_found(
    game: Game, players: list[Participant], player: Participant
):
    game.start()
    game.start_round_voting()

    with pytest.raises(ParticipantNotFoundError):
        game.cast_vote(players[0], player)


def test_cast_vote_eliminates_participant_and_starts_next_round(
    game: Game, players: list[Participant]
):
    game.start()
    game.start_round_voting()

    p1, p2, p3 = players

    game.cast_vote(p1, p3)
    game.cast_vote(p2, p3)
    game.cast_vote(p3, p1)

    assert p3 in game.excluded_participants
    assert p3 not in game.participants

    assert len(game.rounds) == 2
    assert not game.is_finished
    assert game.is_running


def test_game_finishes_when_capacity_reached(players: list[Participant]):
    profile = BunkerProfile(
        catastrophe=Catastrophe(
            name="Virus",
            description="Deadly virus",
            preferred_professions=set(),
            preferred_items=set(),
        ),
        conditions=(),
        time_to_out_years=TimeToOutYears(
            years=10,
            preferred_max_age=40,
        ),
        capacity=2,
    )
    bunker = Bunker(profile)
    game = Game(players.copy(), bunker)
    game.start()

    p1, p2, p3 = players

    game.start_round_voting()
    game.cast_vote(p1, p3)
    game.cast_vote(p2, p3)
    game.cast_vote(p3, p1)

    assert game.is_finished
    assert not game.is_running
    assert game.state == GameState.FINISHED
    assert p3 in game.excluded_participants

    winners = game.winners
    assert tuple(winners) == (p1, p2)
    assert game.bunker.participants == (p1, p2)


def test_finish_not_running(game: Game):
    with pytest.raises(GameNotStartedError):
        game._finish()
