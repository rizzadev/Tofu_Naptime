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
        self.idle_phase = random.uniform(0, math.tau)
        self.interaction_phase = 0
        self.pointer_x = 0
        self.pointer_y = 0
        self.hover_strength = 0.0
        self.hovered = False

        self.canvas.bind("<Motion>", self.on_pointer_move)
        self.canvas.bind("<Leave>", self.on_pointer_leave)

        self.blink_timer = 0
        self.blink = False

        self.zzz = []

        # ==========================================
        # FOOD ANIMATION
        # ==========================================

        self.food_timer = 0
        self.food_x = 0
        self.food_y = 0

    def on_pointer_move(self, event):

        self.pointer_x = event.x
        self.pointer_y = event.y
        self.hovered = self.is_over_tofu(event.x, event.y)

    def on_pointer_leave(self, event):

        self.hovered = False

    def is_over_tofu(self, pointer_x, pointer_y):

        distance_x = (pointer_x - self.state.x) / 120
        distance_y = (pointer_y - self.state.y) / 140

        return distance_x * distance_x + distance_y * distance_y <= 1

    def draw_background_hover(self):

        self.canvas.delete("hover-bg")

        if not 0 <= self.pointer_x <= 1100 or not 0 <= self.pointer_y <= 760:
            return

        pulse = 1 + math.sin(self.interaction_phase) * 0.08
        pointer_x = self.pointer_x
        pointer_y = self.pointer_y

        if pointer_y >= 520:

            radius_x = 72 * pulse
            radius_y = 12 * pulse

            self.canvas.create_oval(
                pointer_x - radius_x,
                pointer_y - radius_y,
                pointer_x + radius_x,
                pointer_y + radius_y,
                fill="#f0c48d",
                outline="",
                stipple="gray25",
                tags="hover-bg"
            )

            self.canvas.create_line(
                pointer_x - 48,
                pointer_y,
                pointer_x + 48,
                pointer_y,
                fill="#f8d8a8",
                width=2,
                stipple="gray50",
                tags="hover-bg"
            )

        else:

            shimmer = 16 + math.sin(self.interaction_phase) * 3

            self.canvas.create_oval(
                pointer_x - shimmer,
                pointer_y - shimmer,
                pointer_x + shimmer,
                pointer_y + shimmer,
                fill="#fff0c2",
                outline="",
                stipple="gray50",
                tags="hover-bg"
            )

    # ==========================================
    # DRAW TOFU
    # ==========================================

    def draw(self):

        canvas = self.canvas
        state = self.state

        canvas.delete("tofu")

        x = state.x
        y = state.y

        target_hover = 1.0 if self.hovered else 0.0
        if self.hover_strength < target_hover:
            self.hover_strength = min(1.0, self.hover_strength + 0.12)
        else:
            self.hover_strength = max(0.0, self.hover_strength - 0.08)

        pointer_dx = max(-4, min(4, (self.pointer_x - x) / 35))
        pointer_dy = max(-3, min(3, (self.pointer_y - y) / 40))
        gaze_x = pointer_dx * self.hover_strength
        gaze_y = pointer_dy * self.hover_strength

        # Small, independent motions keep the pose from looking mechanical.
        idle_sway = math.sin(self.idle_phase) * 1.5
        direction = 1 if state.target_x >= state.x else -1
        y -= 2 * self.hover_strength

        # ==========================================
        # BREATHING
        # ==========================================

        breathing = 0

        if state.sleeping:

            breathing = math.sin(self.breath) * 3.5
            y += math.sin(self.breath * 0.5) * 1.2

        y += breathing + idle_sway

        # ==========================================
        # WALKING
        # ==========================================

        body_move = 0

        if state.walking:

            body_move = math.sin(self.walk) * 3.5

        elif not state.sleeping:

            body_move = math.sin(self.idle_phase * 0.7) * 1.2

        # ==========================================
        # EATING MOVEMENT
        # ==========================================

        eating_move = 0

        if state.eating:

            eating_move = math.sin(self.food_timer * 0.5) * 3

        drinking_move = 0

        if state.drinking:

            drinking_move = math.sin(self.food_timer * 0.35) * 1.8

        eating_move += drinking_move

        # ==========================================
        # TAIL
        # ==========================================

        tail_move = math.sin(self.tail + (0.35 if state.walking else 0)) * (
            11 if state.playing else 6
        )

        canvas.create_line(

            x + 75,

            y + 35 + body_move,

            x + 105 + direction * 4,

            y + 45 + tail_move,

            x + 135,

            y + 20 + tail_move,

            fill="#fff1d6",

            width=26,

            capstyle=tk.ROUND,

            joinstyle=tk.ROUND,

            tags="tofu"
        )

        # A soft contact shadow anchors the character to the floor.
        canvas.create_oval(
            x - 105,
            y + 68,
            x + 105,
            y + 86,
            fill="#9b725d",
            outline="",
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

                y - 28 + body_move + eating_move + gaze_y,

                x - 32 + gaze_x,

                y + 5 + body_move + eating_move + gaze_y,

                fill="#493b45",

                outline="",

                tags="tofu"
            )

            canvas.create_oval(

                x + 8,

                y - 28 + body_move + eating_move + gaze_y,

                x + 38 + gaze_x,

                y + 5 + body_move + eating_move + gaze_y,

                fill="#493b45",

                outline="",

                tags="tofu"
            )

            # Eye highlights

            canvas.create_oval(

                x - 55,

                y - 22 + body_move + eating_move + gaze_y,

                x - 48 + gaze_x,

                y - 15 + body_move + eating_move + gaze_y,

                fill="white",

                outline="",

                tags="tofu"
            )

            canvas.create_oval(

                x + 15,

                y - 22 + body_move + eating_move + gaze_y,

                x + 22 + gaze_x,

                y - 15 + body_move + eating_move + gaze_y,

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

        if self.hover_strength > 0.05:

            whisker_color = "#d99496"
            whisker_shift = math.sin(self.interaction_phase) * 1.5

            canvas.create_line(
                x - 68,
                y + 5 + body_move + eating_move,
                x - 108,
                y - 2 + body_move + eating_move + whisker_shift,
                fill=whisker_color,
                width=2,
                tags="tofu"
            )

            canvas.create_line(
                x + 48,
                y + 5 + body_move + eating_move,
                x + 88,
                y - 2 + body_move + eating_move - whisker_shift,
                fill=whisker_color,
                width=2,
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

            y + 75 + paw_move + drinking_move,

            fill="#fff1d6",

            outline="#dfc9a8",

            width=3,

            tags="tofu"
        )

        if state.walking:

            rear_paw_move = math.sin(self.walk + math.pi) * 6

            canvas.create_oval(
                x - 75,
                y + 42 + rear_paw_move,
                x - 30,
                y + 73 + rear_paw_move,
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
        bounce = math.sin(self.food_timer * 0.35) * 5
        food_sway = math.sin(self.food_timer * 0.18) * 3

        food_x = x + 95 + food_sway

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

            item["x"] += math.sin(item["life"] * 0.12) * 0.25

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

        if self.blink_timer > 115:

            self.blink = True

        if self.blink_timer > 121:

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

        self.breath += 0.10

        self.tail += 0.11 if self.state.playing else 0.07

        self.walk += 0.30 if self.state.walking else 0.08
        self.idle_phase += 0.045
        self.interaction_phase += 0.16 if self.hovered else 0.05

        self.state.update_position()

        self.update_blink()

        self.update_food()

        self.draw_background_hover()

        self.draw()

        self.draw_zzz()

        self.ui.draw_status()

        self.ui.draw_action()

        self.ui.draw_clock()

        self.ui.window.after(
            60,
            self.update
        )