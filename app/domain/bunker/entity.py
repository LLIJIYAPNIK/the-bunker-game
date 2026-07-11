from typing import TypeVar

T = TypeVar("T")


class Bunker[T]:
    def __init__(self):
        self.participants: list[T] = []

    def add_participant(self, participant: T):
        self.participants.append(participant)
