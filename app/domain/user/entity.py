class User:
    def __init__(self, telegram_id, username):
        self.telegram_id = telegram_id
        self.username = username

        self.game_participant = None
