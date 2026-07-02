from enum import Enum, auto


class ParticipantState(Enum):
    ACTIVE = auto()
    OBSERVER = auto()
    LEFT = auto()
