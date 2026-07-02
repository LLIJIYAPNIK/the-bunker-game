from enum import Enum, auto


class GameState(Enum):
    WAITING = auto()
    RUNNING = auto()
    FINISHED = auto()
