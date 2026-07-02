from enum import Enum, auto


class RoundState(Enum):
    DISCUSSION = auto()
    VOTING = auto()
    FINISHED = auto()
