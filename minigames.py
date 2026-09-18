import random


class MiniGames:

    def __init__(self, state):

        self.state = state

    def catch_yarn(self):

        reward = random.randint(5, 15)

        self.state.coins += reward

        self.state.happiness = min(
            100,
            self.state.happiness + 10
        )

        self.state.add_xp(10)

        self.state.action_text = (
            f"Yarn game complete! "
            f"+{reward} coins!"
        )

    def find_mouse(self):

        reward = random.randint(10, 25)

        self.state.coins += reward

        self.state.happiness = min(
            100,
            self.state.happiness + 15
        )

        self.state.add_xp(15)

        self.state.action_text = (
            f"Tofu caught the mouse! "
            f"+{reward} coins!"
        )