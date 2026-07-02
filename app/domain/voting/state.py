from enum import Enum, auto


class VotingState(Enum):
    OPEN = auto()
    COUNTING = auto()
    REVOTE = auto()
    FINISHED = auto()
