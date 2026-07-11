from dataclasses import dataclass


@dataclass(frozen=True)
class VotingResult[T]:
    winners: list[T]

    @property
    def needs_revote(self):
        return len(self.winners) > 1
