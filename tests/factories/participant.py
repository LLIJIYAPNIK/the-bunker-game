from app.domain import character, game

default_character = character.Character(
    age=25,
    blood_group=1,
    gender="male",
    health="strong",
    height=189.4,
    hobby="programming",
    qualities="funny",
    inventory="tea",
    phobia="nothing",
    profession="programmer",
    weight=73.0,
    worldview="Komu",
)


def make_participant(
    user_info: str = "123",
    character_param: character.Character = default_character,
) -> game.Participant:
    return game.Participant(user_info, character_param)
