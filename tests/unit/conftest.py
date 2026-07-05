import pytest

from tests.unit import fakes


@pytest.fixture
def players():
    return [
        fakes.Participant("Alex"),
        fakes.Participant("Dmitriy"),
        fakes.Participant("Vasya"),
    ]
