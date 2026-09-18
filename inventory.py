class Inventory:

    def __init__(self):

        self.items = {

            "Fish": 3,

            "Milk": 2,

            "Yarn": 1,

            "Ball": 1,

            "Mouse Toy": 1
        }

    def add(self, item, amount=1):

        if item not in self.items:

            self.items[item] = 0

        self.items[item] += amount

    def remove(self, item, amount=1):

        if self.items.get(item, 0) < amount:

            return False

        self.items[item] -= amount

        return True

    def has(self, item):

        return self.items.get(item, 0) > 0

    def get_amount(self, item):

        return self.items.get(item, 0)