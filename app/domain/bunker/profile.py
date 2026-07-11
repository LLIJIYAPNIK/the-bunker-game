from collections.abc import Callable
from dataclasses import dataclass


@dataclass(frozen=True)
class SurvivalFactor:
    name: str
    description: str
    preferred_professions: set[str]
    preferred_items: set[str]

    def values_profession(self, profession: str) -> bool:
        return profession in self.preferred_professions

    def values_item(self, item: str) -> bool:
        return item in self.preferred_items


@dataclass(frozen=True)
class Catastrophe(SurvivalFactor):
    pass


@dataclass(frozen=True)
class Condition(SurvivalFactor):
    pass


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

    def is_profession_valuable(self, profession: str) -> bool:
        return self.catastrophe.values_profession(profession) or any(
            c.values_profession(profession) for c in self.conditions
        )

    def is_item_valuable(self, item: str) -> bool:
        return self.catastrophe.values_item(item) or any(
            c.values_item(item) for c in self.conditions
        )
