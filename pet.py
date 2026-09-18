class Pet:

    def __init__(self, state):

        self.state = state

    def feed(self):

        self.state.feed()

    def drink(self):

        self.state.drink()

    def pet(self):

        self.state.pet()

    def play(self, target):

        self.state.play(target)

    def sleep(self):

        self.state.sleep()

    def wake(self):

        self.state.wake()