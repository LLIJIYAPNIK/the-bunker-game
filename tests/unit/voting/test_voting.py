import pytest

from app.domain.voting import (
    TargetDoesNotExistsError,
    VoterAlreadyVotedError,
    VoterSameTargetError,
    Voting,
    VotingClosedError,
    VotingResult,
    VotingState,
)
from tests.unit import fakes


@pytest.fixture
def create_voting(players):
    def _create():
        p1, p2, p3 = players
        p4 = fakes.Participant("abc")
        voting = Voting(voters=[p1, p2, p3, p4], targets=[p1, p2, p3, p4])
        return voting, p1, p2, p3, p4

    return _create


@pytest.fixture
def process_success_voting(create_voting):
    def _create():
        voting, p1, p2, p3, p4 = create_voting()

        voting.register_vote(p1, p2)
        voting.register_vote(p2, p1)
        voting.register_vote(p3, p2)
        res = voting.register_vote(p4, p2)

        return res, voting

    return _create


@pytest.fixture
def process_voting_tie(create_voting):
    def _create():
        voting, p1, p2, p3, p4 = create_voting()

        voting.register_vote(p1, p2)
        voting.register_vote(p2, p3)
        voting.register_vote(p3, p2)
        res = voting.register_vote(p4, p3)

        return res, voting

    return _create


def test_successful_voting(players):
    p1, p2, p3 = players
    voting = Voting(voters=[p1, p2, p3], targets=[p1, p2, p3])
    assert voting.state == VotingState.OPEN

    res1 = voting.register_vote(p1, p2)
    assert voting.state == VotingState.COUNTING
    assert res1 is None

    res2 = voting.register_vote(p2, p3)
    assert voting.state == VotingState.COUNTING
    assert res2 is None

    res3 = voting.register_vote(p3, p2)
    assert voting.state == VotingState.FINISHED
    assert isinstance(res3, VotingResult)
    assert res3.winners == [p2]
    assert not res3.needs_revote


def test_vote_in_closed_voting(players):
    p1, p2, p3 = players
    voting = Voting(voters=[p1, p2, p3], targets=[p1, p2, p3])
    voting.state = VotingState.FINISHED

    with pytest.raises(VotingClosedError):
        voting.register_vote(p1, p2)


def test_participant_voting_again(players):
    p1, p2, p3 = players
    voting = Voting(voters=[p1, p2, p3], targets=[p1, p2, p3])

    res1 = voting.register_vote(p1, p2)
    assert res1 is None

    with pytest.raises(VoterAlreadyVotedError):
        voting.register_vote(p1, p2)


def test_participant_not_exists(players):
    p1, p2, p3 = players
    players.remove(p3)
    voting = Voting(voters=[p1, p2], targets=[p1, p2])

    with pytest.raises(TargetDoesNotExistsError):
        voting.register_vote(p1, p3)
    with pytest.raises(TargetDoesNotExistsError):
        voting.register_vote(p2, fakes.Participant("abc"))


def test_voter_same_target():
    p1 = fakes.Participant("abc")
    voting = Voting(voters=[p1], targets=[p1])

    with pytest.raises(VoterSameTargetError):
        voting.register_vote(p1, p1)


def test_many_winners(process_voting_tie):
    result, voting = process_voting_tie()

    assert isinstance(result, VotingResult)
    assert voting.state == VotingState.FINISHED
    assert isinstance(result, VotingResult)
    assert len(result.winners) > 1
    assert result.needs_revote


def test_revote(process_voting_tie, process_success_voting, players):
    result, voting = process_voting_tie()

    voting.restart()
    assert voting.state == VotingState.REVOTE

    p1, p2, p3 = players
    assert voting.targets == [p2, p3]
    assert voting.votes == {}
    assert voting.voted.keys() != [p1, p2, p3]

    target = voting.targets[0]
    p1, p2, p3, p4 = voting.voted.keys()
    assert voting.voted == {voter: False for voter in voting.voted.keys()}

    voting.register_vote(p1, target)
    voting.register_vote(p2, p3)
    voting.register_vote(p3, p2)
    result = voting.register_vote(p4, target)

    assert voting.state == VotingState.FINISHED
    assert isinstance(result, VotingResult)
    assert result.winners == [target]
    assert not result.needs_revote
