from app.domain import DomainError


class RoundError(DomainError):
    pass


class RoundStateError(RoundError):
    pass


class VotingInDiscussionRoundError(RoundStateError):
    def __init__(self):
        super().__init__("Round is in discussion")


class VotingInFinishedRoundError(RoundStateError):
    def __init__(self):
        super().__init__("Round is finished")
