import tkinter as tk
import random


# -----------------------------
# Main window
# -----------------------------
window = tk.Tk()
window.title("Tofu's Dreamy Nap")
window.geometry("380x460")
window.resizable(False, False)
window.configure(bg="#eee7ff")


# -----------------------------
# App variables
# -----------------------------
mood = "Sleepy"
energy = 60
affection = 12
sleeping = True
breathing_up = True
breathing_size = 32
zzz_size = 16
blink_count = 0


# -----------------------------
# Helper functions
# -----------------------------
def update_status():
    mood_label.config(text=f"Mood: {mood}")
    energy_label.config(text=f"Energy: {'█' * (energy // 10)}{'░' * (10 - energy // 10)}")
    affection_label.config(text=f"Affection: ♥ {affection}")


def set_message(text):
    message_label.config(text=text)


# -----------------------------
# Tofu animation
# -----------------------------
def animate_breathing():
    global breathing_up, breathing_size

    if sleeping:
        if breathing_up:
            breathing_size += 1
            if breathing_size >= 36:
                breathing_up = False
        else:
            breathing_size -= 1
            if breathing_size <= 32:
                breathing_up = True

        cat_label.config(font=("Arial", breathing_size))
    
    window.after(180, animate_breathing)


def animate_zzz():
    global zzz_size

    if sleeping:
        if zzz_size >= 26:
            zzz_size = 16
        else:
            zzz_size += 1

        zzz_label.config(
            text=random.choice(["Z", "Zz", "Zzz"]),
            font=("Arial", zzz_size, "bold")
        )
        zzz_label.place(x=245, y=100)

    else:
        zzz_label.place_forget()

    window.after(500, animate_zzz)


def blink():
    global blink_count

    if not sleeping:
        cat_label.config(text=" /\\_/\\\\\n( ^.^ )\n > ^ <")
        window.after(250, open_eyes)
        return

    cat_label.config(text=" /\\_/\\\\\n( -.- )\n > ^ <")
    window.after(250, open_eyes)


def open_eyes():
    if sleeping:
        cat_label.config(text=" /\\_/\\\\\n( -.- )\n > ^ <")
    else:
        cat_label.config(text=" /\\_/\\\\\n( ^.^ )\n > ^ <")

    window.after(random.randint(2500, 5000), blink)


# -----------------------------
# Interactive actions
# -----------------------------
def pet_tofu():
    global mood, affection, energy, sleeping

    sleeping = False
    mood = "Happy"
    affection += 1
    energy = max(energy - 3, 0)

    cat_label.config(text=" /\\_/\\\\\n( ^w^ )\n > ^ <")
    set_message("Tofu likes being petted!")
    update_status()

    window.after(2500, return_to_sleep)


def play_with_tofu():
    global mood, energy, sleeping

    sleeping = False
    mood = "Playful"
    energy = max(energy - 10, 0)

    cat_label.config(text=" /\\_/\\\\\n( >w< )\n > ^ <")
    set_message("Tofu is playing with you!")
    update_status()

    window.after(3000, return_to_sleep)


def sleep_tofu():
    global mood, energy, sleeping

    sleeping = True
    mood = "Sleepy"
    energy = min(energy + 10, 100)

    cat_label.config(text=" /\\_/\\\\\n( -.- )\n > ^ <")
    set_message("Tofu is having a peaceful nap...")
    update_status()


def return_to_sleep():
    sleep_tofu()


def random_action():
    global mood, sleeping

    if sleeping:
        action = random.choice(["stretch", "yawn", "look"])

        sleeping = False

        if action == "stretch":
            mood = "Calm"
            cat_label.config(text=" /\\_/\\\\\n( ^.^ )\n > ^ <")
            set_message("Tofu is stretching...")

        elif action == "yawn":
            mood = "Sleepy"
            cat_label.config(text=" /\\_/\\\\\n( -o- )\n > ^ <")
            set_message("Tofu is yawning...")

        else:
            mood = "Curious"
            cat_label.config(text=" /\\_/\\\\\n( o.o )\n > ^ <")
            set_message("Tofu is looking around...")

        update_status()
        window.after(2500, return_to_sleep)

    window.after(random.randint(7000, 12000), random_action)


# -----------------------------
# UI layout
# -----------------------------
title_label = tk.Label(
    window,
    text="Tofu's Dreamy Nap",
    font=("Arial", 20, "bold"),
    bg="#eee7ff",
    fg="#55446f"
)
title_label.pack(pady=(18, 4))


subtitle_label = tk.Label(
    window,
    text="A tiny companion for your desktop",
    font=("Arial", 10),
    bg="#eee7ff",
    fg="#81749b"
)
subtitle_label.pack()


room_frame = tk.Frame(
    window,
    bg="#dcd0f5",
    width=330,
    height=245
)
room_frame.pack(pady=18)
room_frame.pack_propagate(False)


# Decorative stars
tk.Label(
    room_frame,
    text="✦       ✧       ✦",
    font=("Arial", 15),
    bg="#dcd0f5",
    fg="#8d7aaa"
).pack(pady=12)


zzz_label = tk.Label(
    room_frame,
    text="Z",
    font=("Arial", 18, "bold"),
    bg="#dcd0f5",
    fg="#6d5b8c"
)


cat_label = tk.Label(
    room_frame,
    text=" /\\_/\\\\\n( -.- )\n > ^ <",
    font=("Arial", 32),
    bg="#dcd0f5",
    fg="#5b4636",
    justify="center"
)
cat_label.pack(expand=True)


message_label = tk.Label(
    window,
    text="Tofu is having a peaceful nap...",
    font=("Arial", 12),
    bg="#eee7ff",
    fg="#55446f"
)
message_label.pack(pady=4)


status_frame = tk.Frame(
    window,
    bg="#eee7ff"
)
status_frame.pack(pady=5)


mood_label = tk.Label(
    status_frame,
    text="Mood: Sleepy",
    font=("Arial", 10),
    bg="#eee7ff",
    fg="#55446f"
)
mood_label.grid(row=0, column=0, padx=10)


energy_label = tk.Label(
    status_frame,
    text="Energy: ██████░░░░",
    font=("Arial", 10),
    bg="#eee7ff",
    fg="#55446f"
)
energy_label.grid(row=1, column=0, padx=10)


affection_label = tk.Label(
    status_frame,
    text="Affection: ♥ 12",
    font=("Arial", 10),
    bg="#eee7ff",
    fg="#55446f"
)
affection_label.grid(row=2, column=0, padx=10)


button_frame = tk.Frame(
    window,
    bg="#eee7ff"
)
button_frame.pack(pady=12)


button_style = {
    "font": ("Arial", 10, "bold"),
    "bg": "#c7b5e8",
    "fg": "#443455",
    "activebackground": "#b39bdc",
    "relief": "flat",
    "padx": 12,
    "pady": 7,
    "cursor": "hand2"
}


tk.Button(
    button_frame,
    text="Pet",
    command=pet_tofu,
    **button_style
).grid(row=0, column=0, padx=4)


tk.Button(
    button_frame,
    text="Play",
    command=play_with_tofu,
    **button_style
).grid(row=0, column=1, padx=4)


tk.Button(
    button_frame,
    text="Sleep",
    command=sleep_tofu,
    **button_style
).grid(row=0, column=2, padx=4)


# Clicking Tofu also pets him
cat_label.bind("<Button-1>", lambda event: pet_tofu())


# -----------------------------
# Start animations
# -----------------------------
update_status()
animate_breathing()
animate_zzz()
open_eyes()
random_action()

window.mainloop()