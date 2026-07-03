from dataclasses import dataclass

from app.domain import game


@dataclass(frozen=True)
class RoundResult:
    eliminated: game.Participant
