import random


class TofuState:

    def __init__(self):

        self.x = 470
        self.y = 400

        self.target_x = 470
        self.velocity_x = 0.0

        self.sleeping = True
        self.playing = False
        self.walking = False
        self.eating = False
        self.drinking = False

        self.is_night = True

        self.weather = "Clear"
        self.weather_description = "Clear"
        self.temperature = None

        self.energy = 85
        self.happiness = 75
        self.hunger = 80
        self.thirst = 80

        self.mood = "Sleepy"

        self.coins = 100

        self.xp = 0
        self.level = 1

        self.pet_count = 0

        self.action_text = "Tofu is sleeping..."

    # ==========================================
    # FEED
    # ==========================================

    def feed(self):

        if self.eating:
            return

        if self.hunger >= 100:

            self.action_text = "Tofu is already full!"

            return

        self.sleeping = False
        self.playing = False
        self.walking = False
        self.drinking = False
        self.eating = True

        self.hunger = min(
            100,
            self.hunger + 25
        )

        self.happiness = min(
            100,
            self.happiness + 5
        )

        self.action_text = "Tofu is eating!"

        self.add_xp(5)

        self.update_mood()

    # ==========================================
    # DRINK
    # ==========================================

    def drink(self):

        if self.thirst >= 100:

            self.action_text = "Tofu is not thirsty!"

            return

        self.sleeping = False
        self.playing = False
        self.walking = False
        self.eating = False
        self.drinking = True

        self.thirst = min(
            100,
            self.thirst + 30
        )

        self.happiness = min(
            100,
            self.happiness + 3
        )

        self.action_text = "Tofu is drinking!"

        self.add_xp(5)

        self.update_mood()

    # ==========================================
    # PET
    # ==========================================

    def pet(self):

        self.sleeping = False

        self.happiness = min(
            100,
            self.happiness + 7
        )

        self.pet_count += 1

        self.action_text = "Tofu loves being petted!"

        self.add_xp(3)

        self.update_mood()

    # ==========================================
    # PLAY
    # ==========================================

    def play(self, target_x=None):

        if self.energy < 10:

            self.action_text = (
                "Tofu is too tired to play."
            )

            return

        if target_x is None:

            target_x = random.randint(
                300,
                650
            )

        self.sleeping = False
        self.playing = True
        self.walking = True
        self.eating = False
        self.drinking = False

        self.target_x = max(
            300,
            min(
                650,
                target_x
            )
        )

        self.happiness = min(
            100,
            self.happiness + 10
        )

        self.action_text = "Tofu is playing!"

        self.add_xp(8)

        self.update_mood()

    # ==========================================
    # SLEEP
    # ==========================================

    def sleep(self):

        self.sleeping = True

        self.playing = False
        self.walking = False
        self.eating = False
        self.drinking = False

        self.target_x = self.x

        self.action_text = (
            "Tofu is sleeping..."
        )

        self.update_mood()

    # ==========================================
    # WAKE
    # ==========================================

    def wake(self):

        self.sleeping = False

        self.playing = False
        self.walking = False
        self.eating = False
        self.drinking = False

        self.action_text = (
            "Good morning, Tofu!"
        )

        self.update_mood()

    # ==========================================
    # DAY / NIGHT
    # ==========================================

    def toggle_day_night(self):

        self.is_night = not self.is_night

        if self.is_night:

            self.action_text = (
                "Night has arrived."
            )

        else:

            self.action_text = (
                "A new day begins!"
            )

    # ==========================================
    # WEATHER
    # ==========================================

    def set_weather(self, weather):

        self.weather = weather

        self.weather_description = weather

    def set_real_weather(
        self,
        weather,
        temperature
    ):

        self.weather = weather

        self.weather_description = weather

        self.temperature = temperature

    # ==========================================
    # XP
    # ==========================================

    def add_xp(self, amount):

        self.xp += amount

        required = self.level * 100

        if self.xp >= required:

            self.xp -= required

            self.level += 1

            self.coins += 25

            self.action_text = (
                f"Tofu reached Level "
                f"{self.level}!"
            )

    # ==========================================
    # MOOD
    # ==========================================

    def update_mood(self):

        if self.sleeping:

            self.mood = "Sleepy"

        elif self.hunger < 20:

            self.mood = "Hungry"

        elif self.thirst < 20:

            self.mood = "Thirsty"

        elif self.energy < 20:

            self.mood = "Tired"

        elif self.happiness >= 85:

            self.mood = "Happy"

        elif self.playing:

            self.mood = "Playful"

        else:

            self.mood = "Relaxed"

    # ==========================================
    # NEEDS
    # ==========================================

    def update_needs(self):

        if self.sleeping:

            self.energy = min(
                100,
                self.energy + 0.10
            )

            self.hunger = max(
                0,
                self.hunger - 0.005
            )

            self.thirst = max(
                0,
                self.thirst - 0.008
            )

        else:

            self.energy = max(
                0,
                self.energy - 0.02
            )

            self.hunger = max(
                0,
                self.hunger - 0.015
            )

            self.thirst = max(
                0,
                self.thirst - 0.02
            )

            if not self.playing:

                self.happiness = max(
                    0,
                    self.happiness - 0.004
                )

        if self.playing:

            self.energy = max(
                0,
                self.energy - 0.04
            )

        if self.energy <= 5:

            self.sleep()

            self.action_text = (
                "Tofu became too tired "
                "and fell asleep."
            )

        self.update_mood()

    # ==========================================
    # MOVEMENT
    # ==========================================

    def update_position(self):

        if not self.walking:
            self.velocity_x *= 0.72
            return

        difference = (
            self.target_x - self.x
        )

        if abs(difference) <= 5:

            self.x = self.target_x
            self.velocity_x = 0.0

            self.walking = False
            self.playing = False

            self.action_text = (
                "Tofu finished playing."
            )

            self.update_mood()

            return

        direction = 1 if difference > 0 else -1
        self.velocity_x += direction * 0.7
        self.velocity_x = max(-3.6, min(3.6, self.velocity_x))
        self.x += self.velocity_x

    # ==========================================
    # RANDOM BEHAVIOR
    # ==========================================

    def random_behavior(self):

        if self.sleeping:
            return

        if self.eating:
            return

        chance = random.random()

        if chance < 0.04:

            self.play()

        elif chance < 0.07:

            self.action_text = (
                "Tofu is looking around."
            )

        elif chance < 0.09:

            self.action_text = (
                "Tofu is relaxing."
            )