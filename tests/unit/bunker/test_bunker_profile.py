import pytest

from app.domain.bunker import (
    BunkerProfile,
    Catastrophe,
    Condition,
    TimeToOutYears,
)


@pytest.fixture
def profile() -> BunkerProfile:
    return BunkerProfile(
        catastrophe=Catastrophe(
            name="Virus",
            description="Deadly virus",
            preferred_professions={"Doctor"},
            preferred_items={"Medicine"},
        ),
        conditions=(
            Condition(
                name="Radiation",
                description="High radiation",
                preferred_professions={"Engineer"},
                preferred_items={"Geiger counter"},
            ),
        ),
        time_to_out_years=TimeToOutYears(
            years=15,
            preferred_max_age=35,
        ),
        capacity=4,
    )


def test_should_value_profession_from_catastrophe(profile: BunkerProfile):
    assert profile.is_profession_valuable("Doctor")


def test_should_value_profession_from_condition(profile: BunkerProfile):
    assert profile.is_profession_valuable("Engineer")


def test_should_not_value_unknown_profession(profile: BunkerProfile):
    assert not profile.is_profession_valuable("Teacher")


def test_should_value_item_from_catastrophe(profile: BunkerProfile):
    assert profile.is_item_valuable("Medicine")


def test_should_value_item_from_condition(profile: BunkerProfile):
    assert profile.is_item_valuable("Geiger counter")


def test_should_not_value_unknown_item(profile: BunkerProfile):
    assert not profile.is_item_valuable("Book")


@pytest.mark.parametrize(
    ("age", "expected"),
    [
        (18, True),
        (35, True),
        (36, False),
        (70, False),
    ],
)
def test_should_check_preferred_age(
    profile: BunkerProfile,
    age: int,
    expected: bool,
):
    assert profile.is_age_valuable(age) is expected
