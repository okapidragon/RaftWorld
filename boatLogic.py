import inventoryLogic as inv

class Boat:
    def __init__(self, durability, size):
        self.durability = durability
        self.size = size  # Size is a tuple (width, height)

    def expand(self, newSize):
        addedArea = (newSize[0] * newSize[1]) - (self.size[0] * self.size[1])

        if addedArea <= 0:
            print("New size must be larger than current size.")
            return False

        self.size = newSize
        print(f"Boat expanded to size: {self.size}")