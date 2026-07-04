from dataclasses import dataclass
from typing import TypeVar

T = TypeVar("T")


@dataclass(frozen=True)
class VotingResult[T]:
    winners: list[T]

    @property
    def needs_revote(self):
        return len(self.winners) > 1
