import pytest

from app.domain.bunker import (
    Bunker,
    BunkerProfile,
    Catastrophe,
    TimeToOutYears,
)
from tests.factories.participant import make_participant


@pytest.fixture
def players():
    return [
        make_participant("Alex"),
        make_participant("Dmitriy"),
        make_participant("Vasya"),
    ]


@pytest.fixture
def player():
    return make_participant("Alex")


@pytest.fixture
def bunker():
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
