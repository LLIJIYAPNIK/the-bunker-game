from app.domain.exceptions import DomainError


class GameError(DomainError):
    pass


class GameAlreadyStartedError(GameError):
    def __init__(self):
        super().__init__("Game is already started")


class GameNotStartedError(GameError):
    def __init__(self):
        super().__init__("Game is not started")


class GameNotFinishedError(GameError):
    def __init__(self):
        super().__init__("Game is not finished")


class ActiveRoundNotFoundError(GameError):
    def __init__(self):
        super().__init__("Active round not found")


class ParticipantNotFoundError(GameError):
    def __init__(self):
        super().__init__("Participant not found")


class RoundNotDiscussionError(GameError):
    def __init__(self):
        super().__init__("Round is not in discussion state")
