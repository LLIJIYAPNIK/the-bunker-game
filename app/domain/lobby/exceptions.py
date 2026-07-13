from app.domain.exceptions import DomainError


class LobbyError(DomainError):
    pass


class ParticipantAlreadyInLobbyError(LobbyError):
    def __init__(self):
        super().__init__("Participant already in lobby")


class ParticipantNotInLobbyError(LobbyError):
    def __init__(self):
        super().__init__("Participant not in lobby")


class LobbyIsStartedError(LobbyError):
    def __init__(self):
        super().__init__("Lobby is started")


class LobbyNotReadyError(LobbyError):
    def __init__(self):
        super().__init__("Lobby is not ready")


class GameNotSetError(LobbyError):
    def __init__(self):
        super().__init__("Game is not set")


class GameIsRunningError(LobbyError):
    def __init__(self):
        super().__init__("Game is running")
