from enum import Enum, auto


class LobbyState(Enum):
    WAITING = auto()
    READY = auto()
    STARTED = auto()
    CLOSED = auto()
