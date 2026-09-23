import os
import sys

os.environ.setdefault("QT_QPA_FONTDIR", r"C:\Windows\Fonts")

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication

from functions import TofuState
from inventory import Inventory
from minigames import MiniGames
from pet import Pet
from pyside_ui import TofuWindow
from save import SaveSystem
from shop import Shop
from weather import Weather


class TofuApp:

    def __init__(self):
        self.qt_app = QApplication(sys.argv)
        self.state = TofuState()
        self.pet = Pet(self.state)
        self.inventory = Inventory()
        self.shop = Shop(self.state, self.inventory)
        self.minigames = MiniGames(self.state)
        self.save_system = SaveSystem(self.state, self.inventory)
        self.weather = Weather(self.state)

        self.window = TofuWindow(self.state)
        self.window.parent_app = self
        self.save_system.load()

        self.needs_timer = QTimer(self.window)
        self.needs_timer.timeout.connect(self.update_needs)
        self.needs_timer.start(1000)

        self.behavior_timer = QTimer(self.window)
        self.behavior_timer.timeout.connect(self.random_behavior)
        self.behavior_timer.start(5000)

        self.weather_timer = QTimer(self.window)
        self.weather_timer.timeout.connect(self.update_weather)
        self.weather_timer.start(30 * 60 * 1000)

    def update_needs(self):
        self.state.update_needs()
        self.window.centralWidget().update()

    def random_behavior(self):
        self.state.random_behavior()
        self.window.centralWidget().update()

    def update_weather(self):
        self.weather.update_weather()
        self.window.centralWidget().update()

    def close(self):
        self.save_system.save()
        self.qt_app.quit()

    def run(self):
        self.window.show()
        return self.qt_app.exec()


if __name__ == "__main__":
    sys.exit(TofuApp().run())
