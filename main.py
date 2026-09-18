import tkinter as tk

from functions import TofuState
from pet import Pet
from inventory import Inventory
from shop import Shop
from minigames import MiniGames
from save import SaveSystem
from weather import Weather
from ui import TofuUI
from animation import TofuAnimation


class TofuApp:

    def __init__(self):

        # ==========================================
        # WINDOW
        # ==========================================

        self.window = tk.Tk()

        self.window.title(
            "Tofu's Dreamy Nap"
        )

        self.window.protocol(
            "WM_DELETE_WINDOW",
            self.close
        )

        # ==========================================
        # STATE
        # ==========================================

        self.state = TofuState()

        # ==========================================
        # PET
        # ==========================================

        self.pet = Pet(
            self.state
        )

        # ==========================================
        # INVENTORY
        # ==========================================

        self.inventory = Inventory()

        # ==========================================
        # SHOP
        # ==========================================

        self.shop = Shop(

            self.state,

            self.inventory
        )

        # ==========================================
        # MINI GAMES
        # ==========================================

        self.minigames = MiniGames(
            self.state
        )

        # ==========================================
        # SAVE SYSTEM
        # ==========================================

        self.save_system = SaveSystem(

            self.state,

            self.inventory
        )

        # ==========================================
        # WEATHER
        # ==========================================

        self.weather = Weather(

            self.state
        )

        # ==========================================
        # UI
        # ==========================================

        self.ui = TofuUI(

            self.window
        )

        # Connect state to UI

        self.ui.set_state(
            self.state
        )

        # ==========================================
        # ANIMATION
        # ==========================================

        self.animation = TofuAnimation(

            self.ui,

            self.state
        )

        # ==========================================
        # INITIAL DISPLAY
        # ==========================================

        self.ui.draw_all()

        # ==========================================
        # LOAD SAVE DATA
        # ==========================================

        self.save_system.load()

        # Redraw after loading

        self.ui.draw_all()

        # ==========================================
        # START ANIMATION
        # ==========================================

        self.animation.update()

        # ==========================================
        # NEEDS TIMER
        # ==========================================

        self.update_needs()

        # ==========================================
        # RANDOM BEHAVIOR TIMER
        # ==========================================

        self.random_behavior()

        # ==========================================
        # WEATHER UPDATE
        # ==========================================

        self.window.after(
            1000,
            self.update_weather
        )

    # ==========================================
    # UPDATE NEEDS
    # ==========================================

    def update_needs(self):

        self.state.update_needs()

        self.window.after(
            1000,
            self.update_needs
        )

    # ==========================================
    # RANDOM BEHAVIOR
    # ==========================================

    def random_behavior(self):

        self.state.random_behavior()

        self.window.after(
            5000,
            self.random_behavior
        )

    # ==========================================
    # WEATHER
    # ==========================================

    def update_weather(self):

        # Run weather update in the background
        # so the UI does not freeze for long.

        self.weather.update_weather()

        self.ui.draw_room()

        self.ui.draw_status()

        self.ui.draw_action()

        self.ui.draw_clock()

        self.window.after(
            30 * 60 * 1000,
            self.update_weather
        )

    # ==========================================
    # CLOSE APPLICATION
    # ==========================================

    def close(self):

        self.save_system.save()

        self.window.destroy()

    # ==========================================
    # RUN
    # ==========================================

    def run(self):

        self.window.mainloop()


# ==============================================
# START PROGRAM
# ==============================================

if __name__ == "__main__":

    app = TofuApp()

    app.run()