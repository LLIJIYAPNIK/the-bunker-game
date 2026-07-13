from enum import Enum, auto


class GameState(Enum):
    WAITING = auto()
    RUNNING = auto()
    FINISHED = auto()


class ParticipantState(Enum):
    READY = auto()
    UNREADY = auto()
