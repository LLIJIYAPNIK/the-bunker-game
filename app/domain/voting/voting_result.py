from dataclasses import dataclass

from app.domain import game


@dataclass(frozen=True)
class VotingResult:
    winners: list[game.Participant]

    @property
    def needs_revote(self):
        return len(self.winners) > 1
