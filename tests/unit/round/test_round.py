import pytest

from app.domain.round import (
    Round,
    RoundResult,
    RoundState,
    VotingInDiscussionRoundError,
    VotingInFinishedRoundError,
)
from app.domain.voting import (
    TargetDoesNotExistsError,
    VoterAlreadyVotedError,
    VoterSameTargetError,
    VotingClosedError,
    VotingState,
)


@pytest.fixture
def game_round(players):
    def _create():
        p1, p2, p3 = players
        return Round([p1, p2, p3])

    return _create


@pytest.fixture
def game_round_4p(players, player):
    def _create():
        p1, p2, p3 = players
        p4 = player
        return Round([p1, p2, p3, p4])

    return _create


@pytest.fixture
def process_game_round_tie(game_round_4p):
    def _create():
        game_round = game_round_4p()
        game_round.start_voting()
        p1, p2, p3, *_ = game_round.voters
        game_round.cast_vote(p1, p2)
        game_round.cast_vote(p2, p3)
        game_round.cast_vote(p3, p2)

        return game_round

    return _create


def test_successful_round(game_round):
    game_round = game_round()

    assert game_round.state == RoundState.DISCUSSION
    assert game_round.voting.state == VotingState.OPEN

    game_round.start_voting()
    assert game_round.state == RoundState.VOTING

    p1, p2, p3 = game_round.voters

    game_round.cast_vote(p1, p2)
    assert game_round.voting.state == VotingState.COUNTING
    game_round.cast_vote(p2, p1)
    result = game_round.cast_vote(p3, p2)

    assert isinstance(result, RoundResult)
    assert result.eliminated == p2
    assert game_round.state == RoundState.FINISHED
    assert game_round.voting.state == VotingState.FINISHED


def test_vote_in_discussion_round(game_round):
    game_round = game_round()
    p1, *_ = game_round.voters

    with pytest.raises(VotingInDiscussionRoundError):
        game_round.cast_vote(p1, p1)


def test_vote_in_finished_round(game_round):
    game_round = game_round()
    game_round.state = RoundState.FINISHED
    p1, *_ = game_round.voters

    with pytest.raises(VotingInFinishedRoundError):
        game_round.cast_vote(p1, p1)


def test_vote_in_closed_voting(game_round):
    game_round = game_round()
    game_round.start_voting()
    game_round.voting.state = VotingState.FINISHED

    p1, p2, *_ = game_round.voters

    with pytest.raises(VotingClosedError):
        game_round.cast_vote(p1, p2)


def test_participant_voting_again(game_round):
    game_round = game_round()
    game_round.start_voting()
    p1, p2, *_ = game_round.voters

    game_round.cast_vote(p1, p2)

    with pytest.raises(VoterAlreadyVotedError):
        game_round.cast_vote(p1, p2)


def test_participant_not_exists(game_round, player):
    game_round = game_round()
    game_round.start_voting()
    p1, p2, *_ = game_round.voters

    with pytest.raises(TargetDoesNotExistsError):
        game_round.cast_vote(p2, player)


def test_voter_same_target(game_round):
    game_round = game_round()
    game_round.start_voting()
    p1, *_ = game_round.voters

    with pytest.raises(VoterSameTargetError):
        game_round.cast_vote(p1, p1)


def test_tie_round(process_game_round_tie):
    game_round = process_game_round_tie()
    p1, p2, p3, p4 = game_round.voters
    game_round.cast_vote(p4, p3)

    assert game_round.voting.state == VotingState.REVOTE
    assert game_round.voting.targets == [p2, p3]
    assert list(game_round.voting.voted.keys()) == [p1, p2, p3, p4]

    game_round.cast_vote(p1, p2)

    with pytest.raises(TargetDoesNotExistsError):
        game_round.cast_vote(p2, p4)

    game_round.cast_vote(p2, p3)
    game_round.cast_vote(p3, p2)
    final = game_round.cast_vote(p4, p2)

    assert isinstance(final, RoundResult)
    assert final.eliminated == p2
    assert game_round.voting.state == VotingState.FINISHED
    assert game_round.state == RoundState.FINISHED
