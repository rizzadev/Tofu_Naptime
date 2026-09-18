import random


class TofuState:

    def __init__(self):

        # ==========================================
        # POSITION
        # ==========================================

        self.x = 450
        self.y = 395

        self.target_x = 450

        # ==========================================
        # BASIC STATE
        # ==========================================

        self.sleeping = True
        self.playing = False
        self.walking = False
        self.drinking = False
        self.eating = False

        # ==========================================
        # WORLD
        # ==========================================

        self.is_night = True

        self.weather = "Clear"
        self.weather_description = "Clear"
        self.temperature = None

        # ==========================================
        # NEEDS
        # ==========================================

        self.energy = 85
        self.happiness = 75
        self.hunger = 80
        self.thirst = 80

        # ==========================================
        # PET INFORMATION
        # ==========================================

        self.mood = "Sleepy"

        self.coins = 100

        self.xp = 0
        self.level = 1

        self.pet_count = 0

        # ==========================================
        # ACTION MESSAGE
        # ==========================================

        self.action_text = "Tofu is sleeping..."

    # ==========================================
    # FEED
    # ==========================================

    def feed(self):

        self.hunger = min(100, self.hunger + 25)
        self.happiness = min(100, self.happiness + 5)

        self.eating = True
        self.drinking = False
        self.playing = False
        self.walking = False
        self.sleeping = False

        self.action_text = "Yum! Tofu is eating!"

        self.add_xp(5)
        self.update_mood()

    # ==========================================
    # DRINK
    # ==========================================

    def drink(self):

        self.thirst = min(100, self.thirst + 30)
        self.happiness = min(100, self.happiness + 3)

        self.drinking = True
        self.eating = False
        self.playing = False
        self.walking = False
        self.sleeping = False

        self.action_text = "Tofu is drinking!"

        self.add_xp(5)
        self.update_mood()

    # ==========================================
    # WAKE
    # ==========================================

    def wake(self):

        self.sleeping = False
        self.playing = False
        self.walking = False
        self.drinking = False
        self.eating = False

        self.action_text = "Good morning, Tofu!"

        self.update_mood()

    # ==========================================
    # SLEEP
    # ==========================================

    def sleep(self):

        self.sleeping = True
        self.playing = False
        self.walking = False
        self.drinking = False
        self.eating = False

        self.target_x = self.x

        self.action_text = "Tofu is sleeping..."

        self.update_mood()

    # ==========================================
    # PLAY
    # ==========================================

    def play(self, target_x):

        if self.energy <= 10:

            self.action_text = "Tofu is too tired to play."

            return

        self.sleeping = False
        self.playing = True
        self.walking = True
        self.drinking = False
        self.eating = False

        self.target_x = max(260, min(650, target_x))

        self.happiness = min(100, self.happiness + 10)

        self.action_text = "Tofu is playing!"

        self.add_xp(8)
        self.update_mood()

    # ==========================================
    # PET
    # ==========================================

    def pet(self):

        self.sleeping = False

        self.happiness = min(100, self.happiness + 7)

        self.pet_count += 1

        self.action_text = "Tofu loves being petted!"

        self.add_xp(3)
        self.update_mood()

    # ==========================================
    # DAY / NIGHT
    # ==========================================

    def toggle_day_night(self):

        self.is_night = not self.is_night

        if self.is_night:

            self.action_text = "Night has arrived."

        else:

            self.action_text = "A new day begins!"

        self.update_mood()

    # ==========================================
    # SET WEATHER
    # ==========================================

    def set_weather(self, weather):

        self.weather = weather
        self.weather_description = weather

        self.action_text = f"The weather is now {weather}."

    # ==========================================
    # REAL WEATHER
    # ==========================================

    def set_real_weather(self, weather, temperature):

        self.weather = weather
        self.weather_description = weather
        self.temperature = temperature

        if temperature is not None:

            self.action_text = (
                f"Real weather: {weather} "
                f"({temperature:.0f}°C)"
            )

        else:

            self.action_text = f"Real weather: {weather}"

    # ==========================================
    # ADD XP
    # ==========================================

    def add_xp(self, amount):

        self.xp += amount

        required = self.level * 100

        if self.xp >= required:

            self.xp -= required

            self.level += 1

            self.coins += 25

            self.action_text = (
                f"Tofu reached Level {self.level}!"
            )

    # ==========================================
    # UPDATE MOOD
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
    # UPDATE NEEDS
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
    # RANDOM BEHAVIOR
    # ==========================================

    def random_behavior(self):

        if self.sleeping:
            return

        chance = random.random()

        if chance < 0.04:

            target = random.randint(300, 600)

            self.play(target)

        elif chance < 0.07:

            self.action_text = "Tofu is looking around."

        elif chance < 0.09:

            self.action_text = "Tofu is relaxing."

    # ==========================================
    # UPDATE POSITION
    # ==========================================

    def update_position(self):

        if not self.walking:
            return

        difference = self.target_x - self.x

        if abs(difference) <= 5:

            self.x = self.target_x

            self.walking = False
            self.playing = False

            self.action_text = (
                "Tofu finished playing."
            )

            self.update_mood()

            return

        if difference > 0:

            self.x += 3

        else:

            self.x -= 3