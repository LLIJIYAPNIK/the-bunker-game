from collections.abc import Callable

from .profile import BunkerProfile, Catastrophe, Condition, TimeToOutYears


class BunkerProfileBuilder:
    def __init__(self):
        self._catastrophe: Catastrophe | None = None
        self._conditions: list[Condition] = []
        self._time_to_out_years: TimeToOutYears | None = None
        self._capacity: int | None = None

    def set_catastrophe(
        self,
        name: str,
        description: str,
        professions: set[str],
        items: set[str],
    ) -> "BunkerProfileBuilder":
        self._catastrophe = Catastrophe(
            name=name,
            description=description,
            preferred_professions=professions,
            preferred_items=items,
        )
        return self

    def add_condition(
        self,
        name: str,
        description: str,
        professions: set[str],
        items: set[str],
    ) -> "BunkerProfileBuilder":
        condition = Condition(
            name=name,
            description=description,
            preferred_professions=professions,
            preferred_items=items,
        )
        self._conditions.append(condition)
        return self

    def set_time_to_out(
        self, years: int, age_predicate: Callable[[int], bool]
    ) -> "BunkerProfileBuilder":
        self._time_to_out_years = TimeToOutYears(
            years=years, preferred_age=age_predicate
        )
        return self

    def set_capacity(self, capacity: int) -> "BunkerProfileBuilder":
        self._capacity = capacity
        return self

    def build(self) -> BunkerProfile:
        if self._catastrophe is None:
            raise ValueError("BunkerProfile require Catastrophe!")
        if self._time_to_out_years is None:
            raise ValueError("BunkerProfile require TimeToOutYears!")
        if self._capacity is None or self._capacity <= 0:
            raise ValueError("Bunker's capacity have to be more than 0!")

        return BunkerProfile(
            catastrophe=self._catastrophe,
            conditions=self._conditions,
            time_to_out_years=self._time_to_out_years,
            capacity=self._capacity,
        )
