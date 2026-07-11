from collections.abc import Callable
from dataclasses import dataclass


@dataclass(frozen=True)
class Catastrophe:
    name: str
    description: str
    preferred_professions: set[str]
    preferred_items: set[str]


@dataclass(frozen=True)
class Condition:
    name: str
    description: str
    preferred_professions: set[str]
    preferred_items: set[str]


@dataclass(frozen=True)
class TimeToOutYears:
    years: int
    preferred_age: Callable[[int], bool]


@dataclass(frozen=True)
class BunkerProfile:
    catastrophe: Catastrophe
    conditions: list[Condition]
    time_to_out_years: TimeToOutYears
    capacity: int
