import tkinter as tk
import math
import random


class TofuAnimation:

    def __init__(self, ui, state):

        self.ui = ui
        self.canvas = ui.canvas
        self.state = state

        # Animation counters
        self.breath = 0
        self.tail = 0
        self.walk = 0

        self.blink_timer = 0
        self.blink = False

        self.zzz = []

        # ==========================================
        # FOOD ANIMATION
        # ==========================================

        self.food_timer = 0
        self.food_x = 0
        self.food_y = 0

    # ==========================================
    # DRAW TOFU
    # ==========================================

    def draw(self):

        canvas = self.canvas
        state = self.state

        canvas.delete("tofu")

        x = state.x
        y = state.y

        # ==========================================
        # BREATHING
        # ==========================================

        breathing = 0

        if state.sleeping:

            breathing = math.sin(
                self.breath
            ) * 4

        y += breathing

        # ==========================================
        # WALKING
        # ==========================================

        body_move = 0

        if state.walking:

            body_move = math.sin(
                self.walk
            ) * 4

        # ==========================================
        # EATING MOVEMENT
        # ==========================================

        eating_move = 0

        if state.eating:

            eating_move = math.sin(
                self.food_timer * 0.5
            ) * 3

        # ==========================================
        # TAIL
        # ==========================================

        tail_move = math.sin(
            self.tail
        ) * 8

        canvas.create_line(

            x + 75,

            y + 35 + body_move,

            x + 105,

            y + 45 + tail_move,

            x + 135,

            y + 20 + tail_move,

            fill="#fff1d6",

            width=26,

            capstyle=tk.ROUND,

            joinstyle=tk.ROUND,

            tags="tofu"
        )

        # ==========================================
        # BODY
        # ==========================================

        canvas.create_oval(

            x - 120,

            y - 60 + body_move,

            x + 120,

            y + 75 + body_move,

            fill="#fff1d6",

            outline="#dfc9a8",

            width=4,

            tags="tofu"
        )

        # ==========================================
        # HEAD
        # ==========================================

        canvas.create_oval(

            x - 100,

            y - 110 + body_move + eating_move,

            x + 70,

            y + 55 + body_move + eating_move,

            fill="#fff1d6",

            outline="#dfc9a8",

            width=4,

            tags="tofu"
        )

        # ==========================================
        # LEFT EAR
        # ==========================================

        canvas.create_polygon(

            x - 85,

            y - 65 + body_move + eating_move,

            x - 70,

            y - 140 + body_move + eating_move,

            x - 20,

            y - 80 + body_move + eating_move,

            fill="#fff1d6",

            outline="#dfc9a8",

            width=4,

            tags="tofu"
        )

        # ==========================================
        # RIGHT EAR
        # ==========================================

        canvas.create_polygon(

            x + 10,

            y - 80 + body_move + eating_move,

            x + 50,

            y - 140 + body_move + eating_move,

            x + 65,

            y - 50 + body_move + eating_move,

            fill="#fff1d6",

            outline="#dfc9a8",

            width=4,

            tags="tofu"
        )

        # ==========================================
        # INNER EARS
        # ==========================================

        canvas.create_polygon(

            x - 72,

            y - 85 + body_move + eating_move,

            x - 68,

            y - 118 + body_move + eating_move,

            x - 43,

            y - 85 + body_move + eating_move,

            fill="#f2a5a5",

            outline="",

            tags="tofu"
        )

        canvas.create_polygon(

            x + 28,

            y - 87 + body_move + eating_move,

            x + 48,

            y - 118 + body_move + eating_move,

            x + 55,

            y - 70 + body_move + eating_move,

            fill="#f2a5a5",

            outline="",

            tags="tofu"
        )

        # ==========================================
        # EYES
        # ==========================================

        if state.sleeping or self.blink:

            # Closed eyes

            canvas.create_arc(

                x - 65,

                y - 25 + body_move + eating_move,

                x - 30,

                y + 5 + body_move + eating_move,

                start=200,

                extent=140,

                style=tk.ARC,

                outline="#55434e",

                width=4,

                tags="tofu"
            )

            canvas.create_arc(

                x + 5,

                y - 25 + body_move + eating_move,

                x + 40,

                y + 5 + body_move + eating_move,

                start=200,

                extent=140,

                style=tk.ARC,

                outline="#55434e",

                width=4,

                tags="tofu"
            )

        else:

            # Open eyes

            canvas.create_oval(

                x - 62,

                y - 28 + body_move + eating_move,

                x - 32,

                y + 5 + body_move + eating_move,

                fill="#493b45",

                outline="",

                tags="tofu"
            )

            canvas.create_oval(

                x + 8,

                y - 28 + body_move + eating_move,

                x + 38,

                y + 5 + body_move + eating_move,

                fill="#493b45",

                outline="",

                tags="tofu"
            )

            # Eye highlights

            canvas.create_oval(

                x - 55,

                y - 22 + body_move + eating_move,

                x - 48,

                y - 15 + body_move + eating_move,

                fill="white",

                outline="",

                tags="tofu"
            )

            canvas.create_oval(

                x + 15,

                y - 22 + body_move + eating_move,

                x + 22,

                y - 15 + body_move + eating_move,

                fill="white",

                outline="",

                tags="tofu"
            )

        # ==========================================
        # NOSE
        # ==========================================

        canvas.create_oval(

            x - 6,

            y - 8 + body_move + eating_move,

            x + 8,

            y + 3 + body_move + eating_move,

            fill="#a86573",

            outline="",

            tags="tofu"
        )

        # ==========================================
        # MOUTH
        # ==========================================

        if state.eating:

            # Open mouth while eating

            canvas.create_oval(

                x - 10,

                y + 2 + body_move + eating_move,

                x + 12,

                y + 20 + body_move + eating_move,

                fill="#8a5965",

                outline="",

                tags="tofu"
            )

            # Small tongue

            canvas.create_oval(

                x - 5,

                y + 11 + body_move + eating_move,

                x + 7,

                y + 18 + body_move + eating_move,

                fill="#e99ba9",

                outline="",

                tags="tofu"
            )

        else:

            canvas.create_arc(

                x - 5,

                y - 2 + body_move + eating_move,

                x + 8,

                y + 15 + body_move + eating_move,

                start=180,

                extent=180,

                style=tk.ARC,

                outline="#8a5965",

                width=2,

                tags="tofu"
            )

        # ==========================================
        # CHEEKS
        # ==========================================

        canvas.create_oval(

            x - 82,

            y - 3 + body_move + eating_move,

            x - 55,

            y + 10 + body_move + eating_move,

            fill="#f3b2b2",

            outline="",

            tags="tofu"
        )

        canvas.create_oval(

            x + 35,

            y - 3 + body_move + eating_move,

            x + 62,

            y + 10 + body_move + eating_move,

            fill="#f3b2b2",

            outline="",

            tags="tofu"
        )

        # ==========================================
        # PAWS
        # ==========================================

        paw_move = 0

        if state.walking:

            paw_move = math.sin(
                self.walk
            ) * 7

        canvas.create_oval(

            x - 30,

            y + 40 + paw_move,

            x + 15,

            y + 75 + paw_move,

            fill="#fff1d6",

            outline="#dfc9a8",

            width=3,

            tags="tofu"
        )

        # ==========================================
        # FOOD
        # ==========================================

        self.draw_food()

    # ==========================================
    # FOOD ANIMATION
    # ==========================================

    def draw_food(self):

        self.canvas.delete("food")

        if not self.state.eating:

            return

        x = self.state.x

        y = self.state.y

        # Food moves up and down
        bounce = math.sin(
            self.food_timer * 0.35
        ) * 5

        food_x = x + 95

        food_y = y + 45 + bounce

        # Plate

        self.canvas.create_oval(

            food_x - 28,

            food_y + 20,

            food_x + 28,

            food_y + 32,

            fill="#eee4dc",

            outline="#c7b5aa",

            width=2,

            tags="food"
        )

        # Fish body

        self.canvas.create_oval(

            food_x - 18,

            food_y - 8,

            food_x + 18,

            food_y + 12,

            fill="#e89a7c",

            outline="#b86e59",

            width=2,

            tags="food"
        )

        # Fish tail

        self.canvas.create_polygon(

            food_x - 18,

            food_y,

            food_x - 32,

            food_y - 12,

            food_x - 32,

            food_y + 12,

            fill="#e89a7c",

            outline="#b86e59",

            width=2,

            tags="food"
        )

        # Fish eye

        self.canvas.create_oval(

            food_x + 7,

            food_y - 2,

            food_x + 11,

            food_y + 2,

            fill="#493b45",

            outline="",

            tags="food"
        )

    # ==========================================
    # ZZZ
    # ==========================================

    def create_zzz(self):

        if not self.state.sleeping:

            return

        self.zzz.append({

            "x":
                self.state.x
                + random.randint(70, 110),

            "y":
                self.state.y - 80,

            "life": 0,

            "size":
                random.randint(16, 26)
        })

    def draw_zzz(self):

        self.canvas.delete("zzz")

        for item in self.zzz[:]:

            item["y"] -= 1

            item["life"] += 1

            if item["life"] > 80:

                self.zzz.remove(item)

                continue

            self.canvas.create_text(

                item["x"],

                item["y"],

                text="Z",

                font=(
                    "Arial",
                    item["size"],
                    "bold"
                ),

                fill="#eee6ff",

                tags="zzz"
            )

        if self.state.sleeping:

            if random.random() < 0.04:

                self.create_zzz()

    # ==========================================
    # BLINK
    # ==========================================

    def update_blink(self):

        self.blink_timer += 1

        if self.blink_timer > 100:

            self.blink = True

        if self.blink_timer > 106:

            self.blink = False

            self.blink_timer = 0

    # ==========================================
    # FOOD TIMER
    # ==========================================

    def update_food(self):

        if self.state.eating:

            self.food_timer += 1

            # Eating lasts about 2.5 seconds

            if self.food_timer >= 42:

                self.state.eating = False

                self.food_timer = 0

                self.state.action_text = (
                    "Yum! Tofu finished eating!"
                )

                self.state.update_mood()

        else:

            self.food_timer = 0

    # ==========================================
    # MAIN UPDATE
    # ==========================================

    def update(self):

        self.breath += 0.12

        self.tail += 0.08

        self.walk += 0.25

        self.state.update_position()

        self.update_blink()

        self.update_food()

        self.draw()

        self.draw_zzz()

        self.ui.draw_status()

        self.ui.draw_action()

        self.ui.draw_clock()

        self.ui.window.after(
            60,
            self.update
        )