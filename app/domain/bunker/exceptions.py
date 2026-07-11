from app.domain import DomainError


class BunkerError(DomainError):
    pass


class BuilderError(BunkerError):
    pass


class CatastropheIsNoneError(BuilderError):
    def __init__(self):
        super().__init__("BunkerProfile require Catastrophe!")


class TimeToOutYearsIsNone(BuilderError):
    def __init__(self):
        super().__init__("BunkerProfile require TimeToOutYears!")


class LowCapacityError(BuilderError):
    def __init__(self):
        super().__init__("Bunker's capacity have to be more than 0!")
