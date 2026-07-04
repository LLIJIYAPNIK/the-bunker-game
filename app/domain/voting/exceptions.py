from app.domain import DomainError


class VotingError(DomainError):
    pass


class VoterAlreadyVotedError(VotingError):
    def __init__(self):
        super().__init__("Voter is already voted or does not a member of it")


class TargetDoesNotExistsError(VotingError):
    def __init__(self):
        super().__init__(
            "Target does not exists or does not a member of the voting"
        )


class VoterSameTargetError(VotingError):
    def __init__(self):
        super().__init__("Voter is same as target")


class VotingClosedError(VotingError):
    def __init__(self):
        super().__init__("Voting is closed")
