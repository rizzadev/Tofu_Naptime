import tkinter as tk
from datetime import datetime


class TofuUI:

    def __init__(self, window):

        self.window = window

        self.window.title(
            "Tofu's Dreamy Nap"
        )

        self.window.geometry(
            "1100x760"
        )

        self.window.resizable(
            False,
            False
        )

        self.state = None

        # ==========================================
        # MAIN CANVAS
        # ==========================================

        self.canvas = tk.Canvas(

            self.window,

            width=1100,

            height=760,

            highlightthickness=0,

            bg="#f5e9dc"
        )

        self.canvas.pack()

        # ==========================================
        # BUTTON AREA
        # ==========================================

        self.create_buttons()

    # ==========================================
    # CONNECT STATE
    # ==========================================

    def set_state(self, state):

        self.state = state

    # ==========================================
    # BUTTONS
    # ==========================================

    def create_buttons(self):

        button_frame = tk.Frame(
            self.window,
            bg="#f5e9dc"
        )

        button_frame.place(
            x=730,
            y=610,
            width=340,
            height=120
        )

        button_style = {

            "font": (
                "Arial",
                10,
                "bold"
            ),

            "width": 10,

            "height": 2,

            "relief": "flat",

            "cursor": "hand2"
        }

        self.feed_button = tk.Button(

            button_frame,

            text="🍣 Feed",

            command=self.feed,

            **button_style
        )

        self.feed_button.grid(
            row=0,
            column=0,
            padx=3,
            pady=3
        )

        self.drink_button = tk.Button(

            button_frame,

            text="🥛 Drink",

            command=self.drink,

            **button_style
        )

        self.drink_button.grid(
            row=0,
            column=1,
            padx=3,
            pady=3
        )

        self.pet_button = tk.Button(

            button_frame,

            text="💗 Pet",

            command=self.pet,

            **button_style
        )

        self.pet_button.grid(
            row=0,
            column=2,
            padx=3,
            pady=3
        )

        self.play_button = tk.Button(

            button_frame,

            text="🎾 Play",

            command=self.play,

            **button_style
        )

        self.play_button.grid(
            row=1,
            column=0,
            padx=3,
            pady=3
        )

        self.sleep_button = tk.Button(

            button_frame,

            text="😴 Sleep",

            command=self.sleep,

            **button_style
        )

        self.sleep_button.grid(
            row=1,
            column=1,
            padx=3,
            pady=3
        )

        self.wake_button = tk.Button(

            button_frame,

            text="☀ Wake",

            command=self.wake,

            **button_style
        )

        self.wake_button.grid(
            row=1,
            column=2,
            padx=3,
            pady=3
        )

    # ==========================================
    # BUTTON ACTIONS
    # ==========================================

    def feed(self):

        if self.state:

            self.state.feed()

    def drink(self):

        if self.state:

            self.state.drink()

    def pet(self):

        if self.state:

            self.state.pet()

    def play(self):

        if self.state:

            self.state.play(550)

    def sleep(self):

        if self.state:

            self.state.sleep()

    def wake(self):

        if self.state:

            self.state.wake()

    # ==========================================
    # ROOM
    # ==========================================

    def draw_room(self):

        canvas = self.canvas

        state = self.state

        canvas.delete("room")

        # ==========================================
        # WALL
        # ==========================================

        if state and state.is_night:

            wall_color = "#24233d"

        else:

            wall_color = "#f8e8d7"

        canvas.create_rectangle(

            0,
            0,
            1100,
            520,

            fill=wall_color,

            outline="",

            tags="room"
        )

        # ==========================================
        # FLOOR
        # ==========================================

        canvas.create_rectangle(

            0,
            520,
            1100,
            760,

            fill="#c99f78",

            outline="",

            tags="room"
        )

        # ==========================================
        # FLOOR LINES
        # ==========================================

        for y in range(
            540,
            760,
            35
        ):

            canvas.create_line(

                0,
                y,
                1100,
                y,

                fill="#b78964",

                width=2,

                tags="room"
            )

        # ==========================================
        # WINDOW
        # ==========================================

        if state and state.is_night:

            sky = "#191a35"

        else:

            sky = "#9ed8f0"

        canvas.create_rectangle(

            70,
            70,
            300,
            250,

            fill="#d8b08c",

            outline="#7e5c4a",

            width=8,

            tags="room"
        )

        canvas.create_rectangle(

            90,
            90,
            280,
            230,

            fill=sky,

            outline="",

            tags="room"
        )

        # Window cross

        canvas.create_line(

            185,
            90,
            185,
            230,

            fill="#d8b08c",

            width=6,

            tags="room"
        )

        canvas.create_line(

            90,
            160,
            280,
            160,

            fill="#d8b08c",

            width=6,

            tags="room"
        )

        # ==========================================
        # SUN / MOON
        # ==========================================

        if state and state.is_night:

            canvas.create_oval(

                215,
                105,
                255,
                145,

                fill="#fff4c4",

                outline="",

                tags="room"
            )

            # Stars

            stars = [

                (115, 120),
                (145, 105),
                (240, 180),
                (115, 195),
                (255, 115)
            ]

            for sx, sy in stars:

                canvas.create_oval(

                    sx - 3,
                    sy - 3,
                    sx + 3,
                    sy + 3,

                    fill="#fff4d6",

                    outline="",

                    tags="room"
                )

        else:

            canvas.create_oval(

                215,
                105,
                260,
                150,

                fill="#ffe29a",

                outline="",

                tags="room"
            )

            # Cloud

            canvas.create_oval(
                105,
                110,
                160,
                145,
                fill="white",
                outline="",
                tags="room"
            )

            canvas.create_oval(
                135,
                95,
                195,
                145,
                fill="white",
                outline="",
                tags="room"
            )

            canvas.create_oval(
                170,
                110,
                220,
                145,
                fill="white",
                outline="",
                tags="room"
            )

        # ==========================================
        # CURTAINS
        # ==========================================

        canvas.create_polygon(

            55,
            55,
            110,
            55,
            100,
            265,
            55,
            245,

            fill="#e9b6c2",

            outline="",

            tags="room"
        )

        canvas.create_polygon(

            260,
            55,
            315,
            55,
            315,
            245,
            270,
            265,

            fill="#e9b6c2",

            outline="",

            tags="room"
        )

        # ==========================================
        # BOOKSHELF
        # ==========================================

        canvas.create_rectangle(

            760,
            70,
            930,
            300,

            fill="#9c7054",

            outline="#704b3b",

            width=4,

            tags="room"
        )

        for y in (
            125,
            180,
            235
        ):

            canvas.create_line(

                765,
                y,
                925,
                y,

                fill="#704b3b",

                width=5,

                tags="room"
            )

        # Books

        book_colors = [

            "#e8a6a6",
            "#9ec8a8",
            "#a9bde8",
            "#e8ca8c",
            "#c5a6e8"
        ]

        x = 775

        for color in book_colors:

            canvas.create_rectangle(

                x,
                85,
                x + 22,
                120,

                fill=color,

                outline="",

                tags="room"
            )

            x += 28

        # ==========================================
        # PLANT
        # ==========================================

        canvas.create_rectangle(

            920,
            410,
            975,
            470,

            fill="#d89175",

            outline="",

            tags="room"
        )

        canvas.create_oval(

            895,
            375,
            945,
            430,

            fill="#79a96b",

            outline="",

            tags="room"
        )

        canvas.create_oval(

            930,
            360,
            980,
            430,

            fill="#6e9d65",

            outline="",

            tags="room"
        )

        canvas.create_oval(

            915,
            345,
            955,
            410,

            fill="#8dbb7d",

            outline="",

            tags="room"
        )

        # ==========================================
        # DESK
        # ==========================================

        canvas.create_rectangle(

            710,
            375,
            900,
            405,

            fill="#9c7054",

            outline="",

            tags="room"
        )

        canvas.create_rectangle(

            730,
            405,
            750,
            510,

            fill="#80573f",

            outline="",

            tags="room"
        )

        canvas.create_rectangle(

            860,
            405,
            880,
            510,

            fill="#80573f",

            outline="",

            tags="room"
        )

        # ==========================================
        # LAMP
        # ==========================================

        canvas.create_line(

            800,
            375,
            800,
            325,

            fill="#51424a",

            width=6,

            tags="room"
        )

        canvas.create_polygon(

            770,
            325,
            830,
            325,
            815,
            295,
            785,
            295,

            fill="#f1c879",

            outline="",

            tags="room"
        )

        # ==========================================
        # BED
        # ==========================================

        canvas.create_rectangle(

            330,
            315,
            650,
            500,

            fill="#8c6470",

            outline="#684d59",

            width=5,

            tags="room"
        )

        canvas.create_rectangle(

            345,
            335,
            635,
            490,

            fill="#e8d8e2",

            outline="",

            tags="room"
        )

        # Pillow

        canvas.create_oval(

            370,
            345,
            475,
            395,

            fill="#f7edf2",

            outline="",

            tags="room"
        )

        # ==========================================
        # RUG
        # ==========================================

        canvas.create_oval(

            250,
            485,
            700,
            625,

            fill="#d8b7bd",

            outline="#a8848d",

            width=4,

            tags="room"
        )

        # ==========================================
        # TITLE
        # ==========================================

        canvas.create_text(

            550,
            30,

            text="TOFU'S DREAMY NAP",

            font=(
                "Arial",
                22,
                "bold"
            ),

            fill=(
                "#eee6ff"
                if state and state.is_night
                else "#694d5d"
            ),

            tags="room"
        )

    # ==========================================
    # TOYS
    # ==========================================

    def draw_toys(self):

        canvas = self.canvas

        canvas.delete("toys")

        # Ball

        canvas.create_oval(

            665,
            545,
            710,
            590,

            fill="#f39a9a",

            outline="#b76d6d",

            width=3,

            tags="toys"
        )

        # Yarn

        canvas.create_oval(

            180,
            545,
            225,
            590,

            fill="#d59adf",

            outline="#9c70a8",

            width=3,

            tags="toys"
        )

        # Yarn string

        canvas.create_arc(

            190,
            555,
            250,
            610,

            start=0,

            extent=160,

            style=tk.ARC,

            outline="#9c70a8",

            width=3,

            tags="toys"
        )

        # Mouse toy

        canvas.create_oval(

            720,
            545,
            765,
            575,

            fill="#9c9caa",

            outline="#666675",

            width=3,

            tags="toys"
        )

        canvas.create_oval(

            715,
            540,
            730,
            555,

            fill="#9c9caa",

            outline="#666675",

            tags="toys"
        )

        canvas.create_oval(

            750,
            540,
            765,
            555,

            fill="#9c9caa",

            outline="#666675",

            tags="toys"
        )

    # ==========================================
    # STATUS
    # ==========================================

    def draw_status(self):

        if not self.state:

            return

        canvas = self.canvas

        canvas.delete("status")

        # ==========================================
        # PANEL
        # ==========================================

        canvas.create_rectangle(

            15,
            310,
            245,
            585,

            fill="#fff7f0",

            outline="#d8bca8",

            width=3,

            tags="status"
        )

        canvas.create_text(

            130,
            335,

            text="TOFU STATUS",

            font=(
                "Arial",
                16,
                "bold"
            ),

            fill="#694d5d",

            tags="status"
        )

        # ==========================================
        # BARS
        # ==========================================

        self.create_bar(

            35,
            365,

            "Energy",

            self.state.energy,

            "#8bb8e8"
        )

        self.create_bar(

            35,
            410,

            "Hunger",

            self.state.hunger,

            "#e8b47e"
        )

        self.create_bar(

            35,
            455,

            "Thirst",

            self.state.thirst,

            "#82c6d8"
        )

        self.create_bar(

            35,
            500,

            "Happiness",

            self.state.happiness,

            "#e8a6b5"
        )

        # ==========================================
        # INFORMATION
        # ==========================================

        canvas.create_text(

            35,
            550,

            anchor="w",

            text=(
                f"Mood: {self.state.mood}\n"
                f"Coins: 🪙 {self.state.coins}\n"
                f"Level: {self.state.level}   "
                f"XP: {self.state.xp}/"
                f"{self.state.level * 100}"
            ),

            font=(
                "Arial",
                10,
                "bold"
            ),

            fill="#694d5d",

            tags="status"
        )

    # ==========================================
    # STATUS BAR
    # ==========================================

    def create_bar(
        self,
        x,
        y,
        label,
        value,
        fill_color
    ):

        canvas = self.canvas

        canvas.create_text(

            x,
            y,

            anchor="w",

            text=(
                f"{label}: "
                f"{value:.0f}%"
            ),

            font=(
                "Arial",
                10,
                "bold"
            ),

            fill="#694d5d",

            tags="status"
        )

        # Background

        canvas.create_rectangle(

            x,
            y + 17,

            x + 190,
            y + 30,

            fill="#eaded6",

            outline="",

            tags="status"
        )

        # Value

        width = (
            190
            * max(0, min(100, value))
            / 100
        )

        canvas.create_rectangle(

            x,
            y + 17,

            x + width,
            y + 30,

            fill=fill_color,

            outline="",

            tags="status"
        )

    # ==========================================
    # ACTION MESSAGE
    # ==========================================

    def draw_action(self):

        if not self.state:

            return

        canvas = self.canvas

        canvas.delete("action")

        canvas.create_rectangle(

            280,
            650,
            700,
            710,

            fill="#fff7f0",

            outline="#d8bca8",

            width=2,

            tags="action"
        )

        canvas.create_text(

            490,
            680,

            text=self.state.action_text,

            font=(
                "Arial",
                12,
                "bold"
            ),

            fill="#694d5d",

            width=390,

            tags="action"
        )

    # ==========================================
    # CLOCK / WEATHER
    # ==========================================

    def draw_clock(self):

        if not self.state:

            return

        canvas = self.canvas

        canvas.delete("clock")

        now = datetime.now()

        time_text = now.strftime(
            "%I:%M:%S %p"
        )

        weather_text = (
            self.state.weather
        )

        if self.state.temperature is not None:

            weather_text += (
                f" | "
                f"{self.state.temperature:.0f}°C"
            )

        canvas.create_text(

            930,
            330,

            text=time_text,

            font=(
                "Arial",
                15,
                "bold"
            ),

            fill=(
                "#eee6ff"
                if self.state.is_night
                else "#694d5d"
            ),

            tags="clock"
        )

        canvas.create_text(

            930,
            355,

            text=weather_text,

            font=(
                "Arial",
                11
            ),

            fill=(
                "#eee6ff"
                if self.state.is_night
                else "#694d5d"
            ),

            tags="clock"
        )

    # ==========================================
    # DRAW EVERYTHING
    # ==========================================

    def draw_all(self):

        self.draw_room()

        self.draw_toys()

        self.draw_status()

        self.draw_action()

        self.draw_clock()