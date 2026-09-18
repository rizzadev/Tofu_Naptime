import json
import os


class SaveSystem:

    def __init__(self, state, inventory):

        self.state = state

        self.inventory = inventory

        self.folder = "data"

        self.file = os.path.join(
            self.folder,
            "tofu_data.json"
        )

        os.makedirs(
            self.folder,
            exist_ok=True
        )

    # ==========================================
    # SAVE
    # ==========================================

    def save(self):

        data = {

            "energy": self.state.energy,

            "happiness": self.state.happiness,

            "hunger": self.state.hunger,

            "thirst": self.state.thirst,

            "coins": self.state.coins,

            "xp": self.state.xp,

            "level": self.state.level,

            "is_night": self.state.is_night,

            "weather": self.state.weather,

            "x": self.state.x,

            "inventory": self.inventory.items
        }

        try:

            with open(
                self.file,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    data,
                    file,
                    indent=4
                )

            self.state.action_text = (
                "Tofu's progress saved!"
            )

        except OSError:

            self.state.action_text = (
                "Could not save Tofu's progress."
            )

    # ==========================================
    # LOAD
    # ==========================================

    def load(self):

        if not os.path.exists(self.file):

            return

        try:

            with open(
                self.file,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

            self.state.energy = data.get(
                "energy",
                self.state.energy
            )

            self.state.happiness = data.get(
                "happiness",
                self.state.happiness
            )

            self.state.hunger = data.get(
                "hunger",
                self.state.hunger
            )

            self.state.thirst = data.get(
                "thirst",
                self.state.thirst
            )

            self.state.coins = data.get(
                "coins",
                self.state.coins
            )

            self.state.xp = data.get(
                "xp",
                self.state.xp
            )

            self.state.level = data.get(
                "level",
                self.state.level
            )

            self.state.is_night = data.get(
                "is_night",
                self.state.is_night
            )

            self.state.weather = data.get(
                "weather",
                self.state.weather
            )

            self.state.x = data.get(
                "x",
                self.state.x
            )

            self.inventory.items = data.get(
                "inventory",
                self.inventory.items
            )

            self.state.action_text = (
                "Welcome back, Tofu!"
            )

            self.state.update_mood()

        except (
            json.JSONDecodeError,
            OSError
        ):

            self.state.action_text = (
                "Could not load save data."
            )