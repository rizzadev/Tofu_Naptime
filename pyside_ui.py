import math
from datetime import datetime

from PySide6.QtCore import QPointF, QRectF, QTimer, Qt
from PySide6.QtGui import QColor, QFont, QPainter, QPen, QBrush
from PySide6.QtWidgets import QMainWindow, QPushButton, QWidget


class TofuWindow(QMainWindow):

    def __init__(self, state):
        super().__init__()

        self.state = state
        self.phase = 0.0
        self.pointer = QPointF(-100, -100)
        self.hovered = False
        self.food_timer = 0
        self.hover_strength = 0.0

        self.setWindowTitle("Tofu's Dreamy Nap")
        self.setFixedSize(900, 900)
        self.setCentralWidget(GameView(self))

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tick)
        self.timer.start(16)

    def tick(self):
        self.phase += 0.10
        self.state.update_position()
        if self.state.eating:
            self.food_timer += 1
            if self.food_timer >= 42:
                self.state.eating = False
                self.food_timer = 0
                self.state.action_text = "Yum! Tofu finished eating!"
                self.state.update_mood()
        else:
            self.food_timer = 0
        self.centralWidget().update()

    def closeEvent(self, event):
        self.parent_app.close()
        event.accept()


class GameView(QWidget):

    def __init__(self, window):
        super().__init__(window)

        self.window = window
        self.state = window.state
        self.setMouseTracking(True)
        self.setAttribute(Qt.WidgetAttribute.WA_OpaquePaintEvent)
        self.hover_target = None
        self.drag_target = None
        self.last_pet_phase = -10.0
        self.create_buttons()

    def create_buttons(self):
        actions = (
            ("Feed", self.state.feed, 24, 110),
            ("Drink", self.state.drink, 99, 110),
            ("Pet", self.state.pet, 174, 110),
            ("Play", lambda: self.state.play(470), 24, 148),
            ("Sleep", self.state.sleep, 99, 148),
            ("Wake", self.state.wake, 174, 148),
        )

        for text, callback, x, y in actions:
            button = QPushButton(text, self)
            button.setGeometry(x, y, 68, 32)
            button.clicked.connect(callback)
            button.setStyleSheet(
                "QPushButton {"
                "background: #fff6fb; color: #9a3f75; border: 2px solid #c85b9a;"
                "border-radius: 15px; font: bold 9px 'Segoe UI';"
                "} QPushButton:hover { background: #ffd7ee; border-color: #8f3d82; }"
                "QPushButton:pressed { background: #f3acd6; }"
            )

    def mouseMoveEvent(self, event):
        self.window.pointer = event.position()
        self.window.hovered = self.is_over_tofu(event.position())
        self.hover_target = self.hit_test(event.position())

        if self.drag_target == "toy":
            self.state.target_x = max(300, min(650, event.position().x()))
            self.state.playing = True
            self.state.walking = True
            self.state.action_text = "Tofu is chasing the toy!"
        elif self.drag_target == "food":
            self.state.target_x = max(300, min(650, event.position().x()))
            self.state.walking = True
            self.state.playing = False
            self.state.action_text = "Tofu is following the food!"
        elif self.drag_target == "pet" and self.window.hovered:
            if self.window.phase - self.last_pet_phase > 0.45:
                self.state.pet()
                self.last_pet_phase = self.window.phase

        self.setCursor(
            Qt.CursorShape.CrossCursor
            if self.window.hovered
            else Qt.CursorShape.ArrowCursor
        )
        self.update()

    def leaveEvent(self, event):
        self.window.pointer = QPointF(-100, -100)
        self.window.hovered = False
        self.hover_target = None
        self.update()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() != Qt.MouseButton.LeftButton:
            return

        point = event.position()
        target = self.hit_test(point)
        self.hover_target = target

        if target in ("head", "body", "tail"):
            self.drag_target = "pet"
            self.state.pet()
        elif target == "food":
            self.drag_target = "food"
            self.state.feed()
        elif target == "water":
            self.state.drink()
        elif target == "bed":
            self.state.target_x = 470
            self.state.walking = True
            self.state.playing = False
            self.state.action_text = "Tofu is going to bed."
        elif target in ("toy", "yarn"):
            self.drag_target = "toy"
            self.state.action_text = "Drag the toy for Tofu!"
        elif target == "lamp":
            self.state.toggle_day_night()
        elif target == "plant":
            self.state.action_text = "Tofu is admiring the plant."
        elif target == "window":
            self.state.action_text = f"Weather: {self.state.weather}"
        self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_target = None
            self.state.walking = False if not self.state.playing else self.state.walking
            self.update()

    def is_over_tofu(self, point):
        dx = (point.x() - self.state.x) / 120
        dy = (point.y() - self.state.y) / 140
        return dx * dx + dy * dy <= 1

    def hit_test(self, point):
        x = point.x()
        y = point.y()
        pet_x = self.state.x
        pet_y = self.state.y

        if QRectF(pet_x - 100, pet_y - 120, 170, 105).contains(point):
            return "head"
        if QRectF(pet_x + 65, pet_y + 15, 75, 70).contains(point):
            return "food"
        if QRectF(pet_x - 120, pet_y - 35, 240, 120).contains(point):
            return "body"
        if QRectF(pet_x + 55, pet_y - 5, 125, 85).contains(point):
            return "tail"
        if QRectF(80, 455, 740, 235).contains(point):
            return "bed"
        if QRectF(35, 405, 75, 75).contains(point):
            return "water"
        if QRectF(24, 20, 160, 48).contains(point):
            return "coins"
        for name, bar_y in (("energy", 280), ("hunger", 315), ("thirst", 350), ("happiness", 385)):
            if QRectF(25, bar_y, 210, 38).contains(point):
                return name
        if QRectF(740, 405, 95, 85).contains(point):
            return "toy"
        if QRectF(185, 285, 120, 75).contains(point):
            return "window"
        if QRectF(600, 270, 110, 90).contains(point):
            return "plant"
        if QRectF(790, 180, 90, 100).contains(point):
            return "lamp"
        if 775 <= y <= 857:
            for card_x in (30, 220, 410, 600):
                if QRectF(card_x, 775, 170, 82).contains(point):
                    return "card"
        return None

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.draw_room(painter)
        self.draw_hover_background(painter)
        self.draw_hover_particles(painter)
        self.draw_toys(painter)
        self.draw_status(painter)
        self.draw_pet(painter)
        self.draw_food(painter)
        self.draw_action(painter)
        self.draw_clock(painter)
        self.draw_interaction_overlay(painter)
        painter.end()

    def fill_rect(self, painter, rect, color, radius=0):
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(color))
        if radius:
            painter.drawRoundedRect(QRectF(*rect), radius, radius)
        else:
            painter.drawRect(QRectF(*rect))

    def draw_room(self, painter):
        self.fill_rect(painter, (0, 0, 900, 900), "#f8bfd8")

        painter.setPen(QPen(QColor("#f3a9ca"), 2))
        for row in range(7):
            for column in range(8):
                x = column * 130 + (65 if row % 2 else 0)
                y = 245 + row * 68
                painter.drawLine(x, y, x + 32, y - 20)
                painter.drawLine(x + 32, y - 20, x + 64, y)
                painter.drawLine(x + 64, y, x + 32, y + 20)
                painter.drawLine(x + 32, y + 20, x, y)

        # Soft scalloped canopy inspired by the reference shop facade.
        self.fill_rect(painter, (0, 0, 900, 82), "#d8c9f4")
        for x in range(-20, 940, 80):
            painter.setBrush(QColor("#f7f0ff" if (x // 80) % 2 else "#e6ddfa"))
            painter.setPen(QPen(QColor("#bda7df"), 2))
            painter.drawEllipse(QRectF(x, 36, 100, 72))

        painter.setPen(QPen(QColor("#8d4c6e"), 2))
        painter.drawLine(48, 78, 48, 160)
        painter.drawLine(135, 78, 135, 142)
        painter.setBrush(QColor("#fff0a9"))
        painter.drawPolygon((QPointF(48, 138), QPointF(62, 158), QPointF(48, 153), QPointF(34, 158)))
        painter.setBrush(QColor("#f7c5e6"))
        painter.drawPolygon((QPointF(135, 120), QPointF(150, 142), QPointF(135, 136), QPointF(120, 142)))

        self.fill_rect(painter, (580, 60, 245, 68), "#e99bba", 30)
        painter.setPen(QPen(QColor("#a95178"), 3))
        painter.drawRoundedRect(QRectF(580, 60, 245, 68), 30, 30)
        self.draw_text(painter, 702, 104, "TOFU'S SHOP", "#fff8fc", 23, True, Qt.AlignmentFlag.AlignCenter)

        self.fill_rect(painter, (24, 20, 160, 48), "#fff1f7", 24)
        self.fill_rect(painter, (198, 20, 160, 48), "#fff1f7", 24)
        self.draw_text(painter, 104, 52, f"COINS  {self.state.coins}", "#9a3f75", 13, True, Qt.AlignmentFlag.AlignCenter)
        self.draw_text(painter, 278, 52, f"LV  {self.state.level}", "#9a3f75", 13, True, Qt.AlignmentFlag.AlignCenter)

        # Floorboards and the plush central rug.
        self.fill_rect(painter, (0, 650, 900, 250), "#e99f9e")
        painter.setPen(QPen(QColor("#d9858c"), 2))
        for y in range(670, 900, 32):
            painter.drawLine(0, y, 900, y)
        self.fill_rect(painter, (80, 455, 740, 235), "#c994e9", 72)
        self.fill_rect(painter, (110, 478, 680, 185), "#9185e8", 50)
        painter.setPen(QPen(QColor("#b5b2ff"), 3))
        for x in range(150, 800, 90):
            painter.drawLine(x, 490, x - 20, 650)
        for y in range(510, 650, 42):
            painter.drawLine(125, y, 775, y + 12)

        # Decorative treats float above the stage.
        painter.setPen(QPen(QColor("#9a4f68"), 3))
        painter.setBrush(QColor("#f6c47d"))
        painter.drawEllipse(QRectF(220, 300, 56, 38))
        painter.setBrush(QColor("#fff0a9"))
        painter.drawEllipse(QRectF(620, 285, 48, 48))
        self.draw_text(painter, 450, 230, "A cozy place for Tofu", "#a9577a", 15, True, Qt.AlignmentFlag.AlignCenter)

    def draw_hover_background(self, painter):
        point = self.window.pointer
        if point.x() < 0 or point.y() < 0:
            return
        pulse = 1 + math.sin(self.window.phase) * 0.08
        painter.setPen(Qt.PenStyle.NoPen)
        if point.y() >= 520:
            painter.setBrush(QColor(240, 196, 141, 55))
            painter.drawEllipse(QRectF(point.x() - 72 * pulse, point.y() - 12 * pulse, 144 * pulse, 24 * pulse))
            painter.setPen(QPen(QColor(248, 216, 168, 90), 2))
            painter.drawLine(point.x() - 48, point.y(), point.x() + 48, point.y())
        else:
            radius = 16 + math.sin(self.window.phase) * 3
            painter.setBrush(QColor(255, 240, 194, 45))
            painter.drawEllipse(QRectF(point.x() - radius, point.y() - radius, radius * 2, radius * 2))

    def draw_hover_particles(self, painter):
        point = self.window.pointer
        if point.x() < 0 or point.y() < 0:
            return

        pulse = math.sin(self.window.phase * 2.2)
        painter.setPen(QPen(QColor(255, 255, 255, 150), 2))

        for index, (offset_x, offset_y) in enumerate(((-34, -18), (28, -28), (45, 18), (-42, 27))):
            scale = 1 + math.sin(self.window.phase * 2 + index) * 0.25
            x = point.x() + offset_x * scale
            y = point.y() + offset_y * scale
            size = 5 + pulse * 1.5
            painter.drawLine(x - size, y, x + size, y)
            painter.drawLine(x, y - size, x, y + size)

        if point.y() >= 455:
            painter.setPen(QPen(QColor(255, 235, 255, 130), 2))
            radius = 34 + pulse * 4
            painter.drawEllipse(QRectF(point.x() - radius, point.y() - radius * 0.32, radius * 2, radius * 0.64))

    def draw_interaction_overlay(self, painter):
        target = self.hover_target
        point = self.window.pointer
        if not target or point.x() < 0 or point.y() < 0:
            return

        messages = {
            "head": "Curious Tofu - ears up",
            "body": "Pet Tofu",
            "tail": "Tail wag!",
            "food": "Feed Tofu",
            "water": "Fresh water",
            "bed": "Sleep",
            "toy": "Drag toy to play",
            "yarn": "Drag yarn to play",
            "window": f"Weather: {self.state.weather}",
            "plant": "Tofu likes the leaves",
            "lamp": "Toggle day and night",
            "card": "Choose a Tofu mood",
            "energy": f"Energy: {self.state.energy:.1f}%",
            "hunger": f"Hunger: {self.state.hunger:.1f}%",
            "thirst": f"Thirst: {self.state.thirst:.1f}%",
            "happiness": f"Happiness: {self.state.happiness:.1f}%",
            "coins": f"Coins: {self.state.coins} available",
        }

        label = messages.get(target)
        if label:
            width = max(150, len(label) * 8 + 28)
            x = max(10, min(900 - width - 10, point.x() - width / 2))
            y = max(90, point.y() - 58)
            self.fill_rect(painter, (x, y, width, 34), "#fff6fb", 17)
            painter.setPen(QPen(QColor("#c85b9a"), 2))
            painter.drawRoundedRect(QRectF(x, y, width, 34), 17, 17)
            self.draw_text(painter, x + width / 2, y + 17, label, "#9a3f75", 10, True, Qt.AlignmentFlag.AlignCenter)

        if target == "water":
            painter.setPen(QPen(QColor("#ffffff"), 2))
            for offset in (-12, 0, 12):
                painter.drawLine(point.x() + offset - 4, point.y() - 10, point.x() + offset, point.y() - 16)
        elif target == "lamp":
            painter.setPen(QPen(QColor(255, 242, 170, 180), 3))
            painter.drawEllipse(QRectF(782, 172, 100, 115))
        elif target == "bed":
            painter.setPen(QPen(QColor("#fff0ff"), 3))
            painter.drawRoundedRect(QRectF(80, 455, 740, 235), 72, 72)
        if self.window.hovered:
            painter.setPen(QPen(QColor(255, 255, 255, 160), 2))
            painter.drawLine(point.x(), point.y(), self.state.x, self.state.y)

    def draw_toys(self, painter):
        bounce = math.sin(self.window.phase * 4) * 7 if self.hover_target in ("toy", "yarn") else 0
        painter.setPen(QPen(QColor("#bd6e9a"), 3))
        painter.setBrush(QColor("#fff0b0" if self.hover_target == "toy" else "#f7d8a0"))
        painter.drawEllipse(QRectF(770, 430 + bounce, 34, 34))
        painter.setBrush(QColor("#f39aaf"))
        painter.drawEllipse(QRectF(770, 430 + bounce, 13, 13))
        painter.setBrush(QColor("#b9e5cf"))
        painter.drawEllipse(QRectF(66, 430 + (bounce if self.hover_target == "yarn" else 0), 34, 34))
        painter.setBrush(QColor("#f6c1dc"))
        painter.drawEllipse(QRectF(73, 437 + (bounce if self.hover_target == "yarn" else 0), 20, 20))

    def draw_status(self, painter):
        self.fill_rect(painter, (20, 230, 190, 215), "#fff6fb", 18)
        self.draw_text(painter, 115, 250, "TOFU STATUS", "#a84c7e", 12, True, Qt.AlignmentFlag.AlignCenter)
        for y, label, value, color in (
            (280, "Energy", self.state.energy, "#9ed0f2"),
            (315, "Hunger", self.state.hunger, "#f2b477"),
            (350, "Thirst", self.state.thirst, "#84d2df"),
            (385, "Happy", self.state.happiness, "#ed9bbb"),
        ):
            self.draw_text(painter, 32, y, f"{label} {value:.0f}%", "#9a3f75", 9, True)
            self.fill_rect(painter, (32, y + 14, 160, 9), "#f0dce8", 5)
            self.fill_rect(painter, (32, y + 14, 160 * max(0, min(100, value)) / 100, 9), color, 5)

        self.fill_rect(painter, (0, 700, 900, 200), "#fff0f5")
        painter.setPen(QPen(QColor("#bf4f93"), 2, Qt.PenStyle.DashLine))
        painter.drawLine(0, 700, 900, 700)
        self.fill_rect(painter, (20, 714, 190, 48), "#fff8fb", 22)
        self.fill_rect(painter, (215, 714, 190, 48), "#ec8ac7", 22)
        self.draw_text(painter, 115, 746, "CATS", "#cc568d", 20, True, Qt.AlignmentFlag.AlignCenter)
        self.draw_text(painter, 310, 746, "THEMES", "#fff8fb", 18, True, Qt.AlignmentFlag.AlignCenter)

        cards = ((30, "SLEEPY", "#fff2e8"), (220, "HAPPY", "#fffaf2"), (410, "PLAYFUL", "#d9d4f8"), (600, "DREAMY", "#ffe4f1"))
        for x, label, color in cards:
            card_hovered = QRectF(x, 775, 170, 82).contains(self.window.pointer)
            if card_hovered:
                self.fill_rect(painter, (x - 5, 770, 180, 92), QColor(255, 255, 255, 90), 22)
            self.fill_rect(painter, (x, 775, 170, 82), color, 18)
            painter.setPen(QPen(QColor("#d47da9"), 2))
            painter.drawRoundedRect(QRectF(x, 775, 170, 82), 18, 18)
            if card_hovered:
                painter.setPen(QPen(QColor("#ffffff"), 3))
                painter.drawRoundedRect(QRectF(x + 2, 777, 166, 78), 16, 16)
            self.fill_rect(painter, (x + 25, 822, 120, 26), "#70d94b", 13)
            self.draw_text(painter, x + 85, 835, "SELECT", "#ffffff", 10, True, Qt.AlignmentFlag.AlignCenter)
            self.draw_text(painter, x + 85, 785, label, "#a84c7e", 11, True, Qt.AlignmentFlag.AlignCenter)

    def draw_pet(self, painter):
        x = self.state.x
        y = self.state.y
        hovered = self.window.hovered
        target = 1.0 if hovered else 0.0
        if self.window.hover_strength < target:
            self.window.hover_strength = min(1.0, self.window.hover_strength + 0.12)
        else:
            self.window.hover_strength = max(0.0, self.window.hover_strength - 0.08)
        strength = self.window.hover_strength
        y -= 2 * strength
        body_move = math.sin(self.window.phase * 3) * 3 if self.state.walking else math.sin(self.window.phase) * 1.2
        if self.state.sleeping:
            y += math.sin(self.window.phase) * 3.5
        gaze_x = max(-4, min(4, (self.window.pointer.x() - x) / 35)) * strength
        gaze_y = max(-3, min(3, (self.window.pointer.y() - y) / 40)) * strength

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor("#9b725d"))
        painter.drawEllipse(QRectF(x - 105, y + 68, 210, 18))
        painter.setBrush(QColor("#fff1d6"))
        painter.drawEllipse(QRectF(x + 60, y + 10, 90, 36))
        painter.drawEllipse(QRectF(x - 120, y - 60 + body_move, 240, 135))
        painter.drawEllipse(QRectF(x - 100, y - 110 + body_move, 170, 165))
        painter.setBrush(QColor("#f2a5a5"))
        ear_lift = math.sin(self.window.phase * 2.5) * 4 * strength
        painter.drawPolygon((QPointF(x - 72, y - 85), QPointF(x - 68, y - 118 - ear_lift), QPointF(x - 43, y - 85)))
        painter.drawPolygon((QPointF(x + 28, y - 87), QPointF(x + 48, y - 118 - ear_lift), QPointF(x + 55, y - 70)))

        painter.setBrush(QColor("#493b45"))
        if self.state.sleeping:
            painter.setPen(QPen(QColor("#55434e"), 4))
            painter.drawArc(QRectF(x - 65, y - 25, 35, 30), 200 * 16, 140 * 16)
            painter.drawArc(QRectF(x + 5, y - 25, 35, 30), 200 * 16, 140 * 16)
        else:
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(QRectF(x - 62 + gaze_x, y - 28 + gaze_y, 30, 33))
            painter.drawEllipse(QRectF(x + 8 + gaze_x, y - 28 + gaze_y, 30, 33))
            painter.setBrush(QColor("white"))
            painter.drawEllipse(QRectF(x - 55 + gaze_x, y - 22 + gaze_y, 7, 7))
            painter.drawEllipse(QRectF(x + 15 + gaze_x, y - 22 + gaze_y, 7, 7))

        painter.setBrush(QColor("#a86573"))
        painter.drawEllipse(QRectF(x - 6, y - 8 + body_move, 14, 11))
        painter.setPen(QPen(QColor("#8a5965"), 2))
        painter.drawArc(QRectF(x - 5, y - 2, 13, 17), 180 * 16, 180 * 16)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor("#f3b2b2"))
        painter.drawEllipse(QRectF(x - 82, y - 3, 27, 13))
        painter.drawEllipse(QRectF(x + 35, y - 3, 27, 13))
        painter.setBrush(QColor("#fff1d6"))
        painter.drawEllipse(QRectF(x - 30, y + 40, 45, 35))
        if self.state.walking:
            painter.drawEllipse(QRectF(x - 75, y + 42 + math.sin(self.window.phase * 3 + math.pi) * 6, 45, 31))

        if strength > 0.05:
            painter.setPen(QPen(QColor("#d99496"), 2))
            whisker_wave = math.sin(self.window.phase * 3) * 2.5
            painter.drawLine(x - 68, y + 5, x - 108, y - 2 + whisker_wave)
            painter.drawLine(x + 48, y + 5, x + 88, y - 2 - whisker_wave)
            painter.setPen(QPen(QColor(255, 255, 255, 190), 2))
            painter.drawArc(QRectF(x - 145, y - 145, 290, 290), 25 * 16, 55 * 16)
            painter.drawArc(QRectF(x - 155, y - 155, 310, 310), 205 * 16, 55 * 16)

    def draw_food(self, painter):
        hovered = self.hover_target == "food"
        if not self.state.eating and not hovered:
            return

        x = self.state.x + 95 + math.sin(self.window.food_timer * 0.18) * 3
        y = self.state.y + 45 + math.sin(self.window.food_timer * 0.35) * 5
        painter.setPen(QPen(QColor("#c85b9a" if hovered else "#c7b5aa"), 3 if hovered else 2))
        painter.setBrush(QColor("#fff4fb" if hovered else "#eee4dc"))
        painter.drawEllipse(QRectF(x - 28, y + 20, 56, 12))
        painter.setBrush(QColor("#e89a7c"))
        painter.drawEllipse(QRectF(x - 18, y - 8, 36, 20))
        painter.drawPolygon((QPointF(x - 18, y), QPointF(x - 32, y - 12), QPointF(x - 32, y + 12)))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor("#493b45"))
        painter.drawEllipse(QRectF(x + 7, y - 2, 4, 4))

    def draw_action(self, painter):
        self.fill_rect(painter, (285, 145, 360, 45), "#fff4fa", 22)
        self.draw_text(painter, 465, 174, self.state.action_text, "#a64f7b", 11, True, Qt.AlignmentFlag.AlignCenter)

    def draw_clock(self, painter):
        color = "#9a3f75"
        self.draw_text(painter, 760, 245, datetime.now().strftime("%I:%M %p"), color, 14, True, Qt.AlignmentFlag.AlignCenter)
        weather = self.state.weather
        if self.state.temperature is not None:
            weather += f" | {self.state.temperature:.0f} C"
        self.draw_text(painter, 760, 270, weather, color, 10, False, Qt.AlignmentFlag.AlignCenter)

    def draw_text(self, painter, x, y, text, color, size, bold=False, alignment=Qt.AlignmentFlag.AlignLeft):
        font = QFont("Segoe UI", size)
        font.setBold(bold)
        painter.setFont(font)
        painter.setPen(QPen(QColor(color)))
        painter.drawText(
            QRectF(x - 200, y - 40, 400, 80),
            alignment | Qt.AlignmentFlag.AlignVCenter | Qt.TextFlag.TextWordWrap,
            text,
        )
