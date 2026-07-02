from dataclasses import dataclass

from app.domain.character.state import CharacterState


@dataclass
class Character:
    age: int
    blood_group: int
    gender: str
    health: str
    height: float
    hobby: str
    qualities: str
    inventory: str
    phobia: str
    profession: str
    weight: float
    worldview: str

    state: CharacterState
