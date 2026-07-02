from enum import Enum, auto


class GameParticipantState(Enum):
    ACTIVE = auto()
    OBSERVER = auto()
    LEFT = auto()
