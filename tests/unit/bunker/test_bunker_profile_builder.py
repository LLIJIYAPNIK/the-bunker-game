import pytest

from app.domain.bunker import (
    BunkerProfile,
    BunkerProfileBuilder,
    Catastrophe,
    CatastropheIsNoneError,
    Condition,
    LowCapacityError,
    TimeToOutYears,
    TimeToOutYearsIsNone,
)

CATASTROPHE_DATA = {
    "name": "Ядерная зима",
    "description": "Земля выжжена радиацией...",
    "professions": {"Физик-ядерщик", "Инженер"},
    "items": {"Счетчик Гейгера", "Рация"},
}

CONDITION_DATA = {
    "name": "Сломан генератор",
    "description": "В бункере нет света, нужны электрики.",
    "professions": {"Электрик", "Сварщик"},
    "items": {"Инструменты", "Провода"},
}


@pytest.fixture
def builder():
    return BunkerProfileBuilder()


def test_successful_bunker_profile_build(builder):
    profile = (
        builder.set_catastrophe(**CATASTROPHE_DATA)
        .add_condition(**CONDITION_DATA)
        .set_time_to_out(years=10, preferred_max_age=45)
        .set_capacity(4)
        .build()
    )

    assert isinstance(profile, BunkerProfile)
    assert profile.capacity == 4

    assert isinstance(profile.catastrophe, Catastrophe)
    assert profile.catastrophe.name == CATASTROPHE_DATA["name"]
    assert profile.catastrophe.description == CATASTROPHE_DATA["description"]
    assert (
        profile.catastrophe.preferred_professions
        == CATASTROPHE_DATA["professions"]
    )
    assert profile.catastrophe.preferred_items == CATASTROPHE_DATA["items"]

    assert len(profile.conditions) == 1
    condition = profile.conditions[0]
    assert isinstance(condition, Condition)
    assert condition.name == CONDITION_DATA["name"]
    assert condition.description == CONDITION_DATA["description"]
    assert condition.preferred_professions == CONDITION_DATA["professions"]
    assert condition.preferred_items == CONDITION_DATA["items"]

    assert isinstance(profile.time_to_out_years, TimeToOutYears)
    assert profile.time_to_out_years.years == 10
    assert profile.time_to_out_years.values_age(25) is True
    assert profile.time_to_out_years.values_age(60) is False


def test_build_multiple_conditions(builder):
    profile = (
        builder.set_catastrophe(**CATASTROPHE_DATA)
        .add_condition(
            name="Условие 1", description="...", professions=set(), items=set()
        )
        .add_condition(
            name="Условие 2", description="...", professions=set(), items=set()
        )
        .set_time_to_out(years=1, preferred_max_age=100)
        .set_capacity(2)
        .build()
    )

    assert len(profile.conditions) == 2
    assert profile.conditions[0].name == "Условие 1"
    assert profile.conditions[1].name == "Условие 2"


def test_raise_error_when_catastrophe_is_missing(builder):
    (builder.set_time_to_out(years=5, preferred_max_age=100).set_capacity(4))

    with pytest.raises(CatastropheIsNoneError):
        builder.build()


def test_raise_error_when_time_to_out_is_missing(builder):
    (builder.set_catastrophe(**CATASTROPHE_DATA).set_capacity(4))

    with pytest.raises(TimeToOutYearsIsNone):
        builder.build()


@pytest.mark.parametrize("invalid_capacity", [None, 0, -1, -100])
def test_raise_error_on_invalid_capacity(builder, invalid_capacity):
    builder_chain = builder.set_catastrophe(
        **CATASTROPHE_DATA
    ).set_time_to_out(years=5, preferred_max_age=100)

    if invalid_capacity is not None:
        builder_chain.set_capacity(invalid_capacity)

    with pytest.raises(LowCapacityError):
        builder_chain.build()
