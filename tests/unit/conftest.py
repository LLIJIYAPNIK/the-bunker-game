import pytest

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
