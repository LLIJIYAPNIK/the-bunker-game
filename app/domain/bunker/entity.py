from .exceptions import BunkerOverflowError, ParticipantNotFoundError
from .profile import BunkerProfile


class Bunker[T]:
    def __init__(self, profile: BunkerProfile):
        self.profile = profile
        self._participants: list[T] = []

    @property
    def participants(self) -> tuple[T, ...]:
        return tuple(self._participants)

    @property
    def free_places(self) -> int:
        return self.profile.capacity - len(self._participants)

    @property
    def is_full(self) -> bool:
        return self.free_places == 0

    def add_participant(self, participant: T):
        if self.is_full:
            raise BunkerOverflowError()
        self._participants.append(participant)

    def remove_participant(self, participant: T):
        if not self.has_participant(participant):
            raise ParticipantNotFoundError
        self._participants.remove(participant)

    def has_participant(self, participant: T):
        return participant in self._participants
