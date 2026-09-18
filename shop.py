class Shop:

    def __init__(self, state, inventory):

        self.state = state

        self.inventory = inventory

        self.items = {

            "Fish": 15,

            "Milk": 10,

            "Yarn": 30,

            "Ball": 40,

            "Mouse Toy": 50
        }

    def buy(self, item):

        if item not in self.items:

            return False

        price = self.items[item]

        if self.state.coins < price:

            self.state.action_text = (
                "Not enough coins!"
            )

            return False

        self.state.coins -= price

        self.inventory.add(item)

        self.state.action_text = (
            f"Bought {item}!"
        )

        return True