import inventoryLogic as inv
import imports as imp

class Boat:
    def __init__(self, durability, size):
        self.durability = durability
        self.size = size  # Size is a tuple (width, height)

    def expand(self, newSize):
        addedArea = (newSize[0] * newSize[1]) - (self.size[0] * self.size[1])

        if addedArea <= 0:
            imp.outputMessage.append("New size must be larger than current size.")
            return False

        self.size = newSize
        imp.outputMessage.append(f"Boat expanded to size: {self.size}")

class Player:
    def __init__(self, name, hunger = 100):
        self.name = name
        self.hunger = hunger

    def eat(self, foodResource):
        if foodResource.quantity > 0:
            foodResource.remove(1)
            self.hunger = min(self.hunger + 100, 100)  # Increase hunger but not above 100
            imp.outputMessage.append(f"{self.name} ate {foodResource.name}. Hunger is now {self.hunger}.")
        else:
            imp.outputMessage.append(f"No {foodResource.name} left to eat.")

    def hungerFrame(self):
        self.hunger -= 2

        self.eat(inv.lookup("Fish"))

        if self.hunger <= -100:
            imp.outputMessage.append(f"{self.name} has starved!")