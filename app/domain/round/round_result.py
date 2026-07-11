from dataclasses import dataclass


@dataclass(frozen=True)
class RoundResult[T]:
    eliminated: T
