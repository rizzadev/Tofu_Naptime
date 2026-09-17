import tkinter as tk
import math
import random


# =========================================================
# WINDOW
# =========================================================

window = tk.Tk()
window.title("Tofu's Dreamy Nap")
window.geometry("900x600")
window.resizable(False, False)
window.configure(bg="#292443")


# =========================================================
# CANVAS
# =========================================================

canvas = tk.Canvas(
    window,
    width=900,
    height=600,
    highlightthickness=0
)

canvas.pack()


# =========================================================
# COLORS
# =========================================================

NIGHT_WALL = "#514875"
DAY_WALL = "#d8b9a8"

FLOOR = "#b98f7a"
BED = "#9b82d0"
BED_LIGHT = "#c8b7ed"

TOFU = "#fff4df"
TOFU_SHADOW = "#ead8bd"
EAR = "#f3a6a6"
NOSE = "#9d6170"

PLANT = "#6e9b70"
WOOD = "#8b6250"

WHITE = "#fffaf0"
YELLOW = "#ffe49a"


# =========================================================
# STATE
# =========================================================

is_night = True
tofu_sleeping = True
tofu_playing = False

breath_phase = 0
tail_phase = 0

tofu_x = 450
tofu_y = 390

zzz_particles = []


# =========================================================
# DRAW ROOM
# =========================================================

def draw_room():

    canvas.delete("room")

    wall_color = NIGHT_WALL if is_night else DAY_WALL

    # Wall
    canvas.create_rectangle(
        0, 0, 900, 430,
        fill=wall_color,
        outline="",
        tags="room"
    )

    # Floor
    canvas.create_rectangle(
        0, 430, 900, 600,
        fill=FLOOR,
        outline="",
        tags="room"
    )

    # Floor lines
    for x in range(0, 900, 90):
        canvas.create_line(
            x, 430,
            x + 60, 600,
            fill="#a77d6d",
            width=2,
            tags="room"
        )

    # =====================================================
    # WINDOW
    # =====================================================

    canvas.create_rectangle(
        200, 65, 700, 335,
        fill="#6e658e",
        outline="#3e385d",
        width=8,
        tags="room"
    )

    if is_night:

        # Night sky
        canvas.create_rectangle(
            210, 75, 690, 325,
            fill="#252d58",
            outline="",
            tags="room"
        )

        # Moon
        canvas.create_oval(
            525, 115,
            590, 180,
            fill="#ffe8a8",
            outline="",
            tags="room"
        )

        canvas.create_oval(
            545, 105,
            600, 165,
            fill="#252d58",
            outline="",
            tags="room"
        )

        # Stars
        random.seed(5)

        for i in range(22):

            x = random.randint(235, 665)
            y = random.randint(90, 300)

            canvas.create_oval(
                x,
                y,
                x + 4,
                y + 4,
                fill=WHITE,
                outline="",
                tags="room"
            )

    else:

        # Day sky
        canvas.create_rectangle(
            210, 75, 690, 325,
            fill="#8fc6e8",
            outline="",
            tags="room"
        )

        # Sun
        canvas.create_oval(
            525, 110,
            600, 185,
            fill="#ffe49a",
            outline="",
            tags="room"
        )

        # Clouds
        for x, y in [(280, 130), (315, 120), (350, 135)]:

            canvas.create_oval(
                x - 30,
                y - 15,
                x + 30,
                y + 15,
                fill=WHITE,
                outline="",
                tags="room"
            )

    # Window frame
    canvas.create_line(
        450, 75,
        450, 325,
        fill="#50486f",
        width=7,
        tags="room"
    )

    canvas.create_line(
        210, 200,
        690, 200,
        fill="#50486f",
        width=7,
        tags="room"
    )

    # =====================================================
    # CURTAINS
    # =====================================================

    canvas.create_polygon(
        130, 50,
        220, 50,
        220, 320,
        170, 300,
        130, 330,
        fill="#b79dd9",
        outline="",
        tags="room"
    )

    canvas.create_polygon(
        680, 50,
        770, 50,
        770, 330,
        730, 300,
        680, 320,
        fill="#b79dd9",
        outline="",
        tags="room"
    )

    # =====================================================
    # BOOKSHELF
    # =====================================================

    canvas.create_rectangle(
        15, 115,
        135, 390,
        fill=WOOD,
        outline="#684939",
        width=4,
        tags="room"
    )

    for y in [175, 240, 305]:

        canvas.create_line(
            20, y,
            130, y,
            fill="#684939",
            width=5,
            tags="room"
        )

    book_colors = [
        "#8e78bb",
        "#d58fa5",
        "#7da1bd",
        "#e5c487"
    ]

    for shelf_y in [165, 230, 295]:

        for i in range(5):

            x = 28 + i * 19

            canvas.create_rectangle(
                x,
                shelf_y - 40,
                x + 15,
                shelf_y,
                fill=book_colors[i % 4],
                outline="",
                tags="room"
            )

    # =====================================================
    # TABLE
    # =====================================================

    canvas.create_rectangle(
        760, 290,
        875, 410,
        fill=WOOD,
        outline="#684939",
        width=4,
        tags="room"
    )

    canvas.create_rectangle(
        745, 275,
        890, 305,
        fill="#a8755d",
        outline="",
        tags="room"
    )

    # =====================================================
    # LAMP
    # =====================================================

    canvas.create_oval(
        790, 220,
        845, 275,
        fill=YELLOW if is_night else "#f4d9b1",
        outline="",
        tags="room"
    )

    canvas.create_rectangle(
        812, 270,
        822, 290,
        fill="#6c5360",
        outline="",
        tags="room"
    )

    # =====================================================
    # PLANT
    # =====================================================

    canvas.create_rectangle(
        735, 390,
        790, 425,
        fill="#b77860",
        outline="",
        tags="room"
    )

    leaves = [
        (750, 365),
        (770, 350),
        (785, 370),
        (760, 340),
        (740, 380)
    ]

    for x, y in leaves:

        canvas.create_oval(
            x - 15,
            y - 25,
            x + 15,
            y + 5,
            fill=PLANT,
            outline="",
            tags="room"
        )

    # =====================================================
    # RUG
    # =====================================================

    canvas.create_oval(
        120, 380,
        780, 575,
        fill="#d9c7c1",
        outline="",
        tags="room"
    )

    # =====================================================
    # BED
    # =====================================================

    canvas.create_oval(
        240, 350,
        660, 535,
        fill=BED,
        outline="#7762a7",
        width=5,
        tags="room"
    )

    canvas.create_oval(
        270, 365,
        630, 505,
        fill=BED_LIGHT,
        outline="",
        tags="room"
    )


# =========================================================
# TOFU
# =========================================================

def draw_tofu():

    canvas.delete("tofu")

    if tofu_sleeping:

        breathing = math.sin(breath_phase) * 4

    else:

        breathing = 0

    x = tofu_x
    y = tofu_y + breathing

    # =====================================================
    # TAIL
    # Draw BEFORE body so it looks attached
    # =====================================================

    tail_offset = math.sin(tail_phase) * 6

    canvas.create_line(
        x + 70,
        y + 35 + tail_offset,

        x + 115,
        y + 55 + tail_offset,

        x + 155,
        y + 35 + tail_offset,

        x + 145,
        y + 5 + tail_offset,

        smooth=True,

        fill=TOFU,

        width=30,

        capstyle=tk.ROUND,

        joinstyle=tk.ROUND,

        tags="tofu"
    )

    # =====================================================
    # BODY
    # =====================================================

    canvas.create_oval(
        x - 125,
        y - 65,
        x + 125,
        y + 75,
        fill=TOFU,
        outline=TOFU_SHADOW,
        width=4,
        tags="tofu"
    )

    # =====================================================
    # HEAD
    # =====================================================

    canvas.create_oval(
        x - 105,
        y - 105,
        x + 65,
        y + 55,
        fill=TOFU,
        outline=TOFU_SHADOW,
        width=4,
        tags="tofu"
    )

    # =====================================================
    # EARS
    # =====================================================

    canvas.create_polygon(
        x - 90, y - 65,
        x - 75, y - 135,
        x - 25, y - 80,

        fill=TOFU,

        outline=TOFU_SHADOW,

        width=4,

        tags="tofu"
    )

    canvas.create_polygon(
        x + 10, y - 80,
        x + 50, y - 135,
        x + 65, y - 50,

        fill=TOFU,

        outline=TOFU_SHADOW,

        width=4,

        tags="tofu"
    )

    # Inner ears

    canvas.create_polygon(
        x - 78, y - 80,
        x - 72, y - 118,
        x - 45, y - 85,

        fill=EAR,

        outline="",

        tags="tofu"
    )

    canvas.create_polygon(
        x + 25, y - 85,
        x + 47, y - 117,
        x + 55, y - 70,

        fill=EAR,

        outline="",

        tags="tofu"
    )

    # =====================================================
    # FACE
    # =====================================================

    if tofu_sleeping:

        # Closed eyes

        canvas.create_arc(
            x - 65,
            y - 25,
            x - 30,
            y + 5,

            start=200,
            extent=140,

            style=tk.ARC,

            outline="#574451",

            width=4,

            tags="tofu"
        )

        canvas.create_arc(
            x + 5,
            y - 25,
            x + 40,
            y + 5,

            start=200,
            extent=140,

            style=tk.ARC,

            outline="#574451",

            width=4,

            tags="tofu"
        )

    else:

        # Open eyes

        canvas.create_oval(
            x - 62,
            y - 28,
            x - 32,
            y + 5,

            fill="#4c3c4a",

            outline="",

            tags="tofu"
        )

        canvas.create_oval(
            x + 8,
            y - 28,
            x + 38,
            y + 5,

            fill="#4c3c4a",

            outline="",

            tags="tofu"
        )

        # Eye highlights

        canvas.create_oval(
            x - 55,
            y - 23,
            x - 48,
            y - 16,

            fill=WHITE,

            outline="",

            tags="tofu"
        )

        canvas.create_oval(
            x + 15,
            y - 23,
            x + 22,
            y - 16,

            fill=WHITE,

            outline="",

            tags="tofu"
        )

    # Nose

    canvas.create_oval(
        x - 5,
        y - 8,
        x + 8,
        y + 3,

        fill=NOSE,

        outline="",

        tags="tofu"
    )

    # Mouth

    canvas.create_arc(
        x - 5,
        y - 2,
        x + 8,
        y + 15,

        start=180,
        extent=180,

        style=tk.ARC,

        outline="#8a5965",

        width=2,

        tags="tofu"
    )

    # =====================================================
    # BLUSH
    # =====================================================

    canvas.create_oval(
        x - 82,
        y - 3,
        x - 55,
        y + 10,

        fill="#f4b4b5",

        outline="",

        tags="tofu"
    )

    canvas.create_oval(
        x + 35,
        y - 3,
        x + 62,
        y + 10,

        fill="#f4b4b5",

        outline="",

        tags="tofu"
    )

    # =====================================================
    # PAW
    # =====================================================

    canvas.create_oval(
        x - 30,
        y + 40,
        x + 15,
        y + 75,

        fill=TOFU,

        outline=TOFU_SHADOW,

        width=3,

        tags="tofu"
    )


# =========================================================
# ZZZ
# =========================================================

def create_zzz():

    if not tofu_sleeping:
        return

    particle = {
        "x": tofu_x + random.randint(70, 110),
        "y": tofu_y - 80,
        "size": random.randint(16, 26),
        "life": 0
    }

    zzz_particles.append(particle)


def animate_zzz():

    canvas.delete("zzz")

    for particle in zzz_particles[:]:

        particle["y"] -= 1.2

        particle["x"] += math.sin(
            particle["life"] / 10
        ) * 0.5

        particle["life"] += 1

        if particle["life"] > 80:

            zzz_particles.remove(particle)

            continue

        canvas.create_text(
            particle["x"],
            particle["y"],

            text="Z",

            font=(
                "Arial",
                particle["size"],
                "bold"
            ),

            fill="#eee6ff",

            tags="zzz"
        )

    if tofu_sleeping:

        if random.random() < 0.04:
            create_zzz()

    window.after(
        50,
        animate_zzz
    )


# =========================================================
# TOFU ANIMATION
# =========================================================

def animate_tofu():

    global breath_phase
    global tail_phase

    breath_phase += 0.12
    tail_phase += 0.08

    draw_tofu()

    window.after(
        60,
        animate_tofu
    )


# =========================================================
# INTERACTION
# =========================================================

def wake_tofu(event=None):

    global tofu_sleeping
    global tofu_playing

    tofu_sleeping = False
    tofu_playing = False

    draw_tofu()


def sleep_tofu(event=None):

    global tofu_sleeping
    global tofu_playing

    tofu_sleeping = True
    tofu_playing = False

    draw_tofu()


def play_with_yarn(event=None):

    global tofu_sleeping
    global tofu_playing

    tofu_sleeping = False
    tofu_playing = True

    draw_tofu()

    move_tofu_to_yarn()


def move_tofu_to_yarn():

    global tofu_x

    if tofu_x > 330:

        tofu_x -= 3

        window.after(
            40,
            move_tofu_to_yarn
        )


def toggle_day_night(event=None):

    global is_night

    is_night = not is_night

    draw_room()


# =========================================================
# INTERACTIVE OBJECTS
# =========================================================

def draw_interactive_objects():

    # =====================================================
    # YARN
    # =====================================================

    canvas.create_oval(
        105, 465,
        175, 535,

        fill="#c57ac7",

        outline="#87528e",

        width=3,

        tags="yarn"
    )

    for i in range(4):

        canvas.create_arc(
            110 + i * 5,
            470,
            170,
            530,

            start=i * 40,

            extent=130,

            style=tk.ARC,

            outline="#f0b5e8",

            width=2,

            tags="yarn"
        )

    # =====================================================
    # FISH
    # =====================================================

    canvas.create_oval(
        700, 470,
        770, 510,

        fill="#7da8d4",

        outline="#4f759e",

        width=3,

        tags="fish"
    )

    canvas.create_polygon(
        700, 490,
        675, 470,
        675, 510,

        fill="#7da8d4",

        outline="#4f759e",

        width=3,

        tags="fish"
    )

    canvas.create_oval(
        748, 480,
        755, 487,

        fill="#30283d",

        outline="",

        tags="fish"
    )


# =========================================================
# CLICK EVENTS
# =========================================================

canvas.tag_bind(
    "tofu",
    "<Button-1>",
    wake_tofu
)

canvas.tag_bind(
    "yarn",
    "<Button-1>",
    play_with_yarn
)

canvas.tag_bind(
    "fish",
    "<Button-1>",
    play_with_yarn
)

canvas.bind(
    "<Double-Button-1>",
    sleep_tofu
)

window.bind(
    "<KeyPress-l>",
    toggle_day_night
)


# =========================================================
# START
# =========================================================

draw_room()

draw_interactive_objects()

draw_tofu()

animate_tofu()

animate_zzz()

window.mainloop()