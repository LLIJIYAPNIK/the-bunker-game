import pytest

from app.domain.bunker import (
    Bunker,
    BunkerOverflowError,
    BunkerProfile,
    Catastrophe,
    ParticipantNotFoundError,
    TimeToOutYears,
)


@pytest.fixture
def bunker() -> Bunker[str]:
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

    return Bunker(profile)


def test_should_have_no_participants_initially(bunker: Bunker[str]):
    assert bunker.participants == ()
    assert bunker.free_places == 2
    assert not bunker.is_full


def test_should_add_participant(bunker: Bunker[str]):
    bunker.add_participant("Alice")

    assert bunker.participants == ("Alice",)
    assert bunker.has_participant("Alice")


def test_should_reduce_number_of_free_places_after_adding_participant(
    bunker: Bunker[str],
):
    bunker.add_participant("Alice")

    assert bunker.free_places == 1


def test_should_be_full_when_capacity_is_reached(
    bunker: Bunker[str],
):
    bunker.add_participant("Alice")
    bunker.add_participant("Bob")

    assert bunker.is_full
    assert bunker.free_places == 0


def test_should_raise_when_bunker_overflows(
    bunker: Bunker[str],
):
    bunker.add_participant("Alice")
    bunker.add_participant("Bob")

    with pytest.raises(BunkerOverflowError):
        bunker.add_participant("Charlie")


def test_should_remove_participant(
    bunker: Bunker[str],
):
    bunker.add_participant("Alice")

    bunker.remove_participant("Alice")

    assert not bunker.has_participant("Alice")
    assert bunker.participants == ()


def test_should_raise_when_participant_not_found(
    bunker: Bunker[str],
):
    with pytest.raises(ParticipantNotFoundError):
        bunker.remove_participant("Alice")


def test_should_increase_number_of_free_places_after_removing_participant(
    bunker: Bunker[str],
):
    bunker.add_participant("Alice")

    bunker.remove_participant("Alice")

    assert bunker.free_places == 2
