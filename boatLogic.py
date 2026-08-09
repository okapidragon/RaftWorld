import inventoryLogic as inv

class Boat:
    def __init__(self, durability, size=(3,6)):
        self.durability = durability
        self.size = size  # Size is a tuple (width, height)

    def expand(self, newSize):
        costWood = (newSize[0] * newSize[1]) - (self.size[0] * self.size[1])

        if costWood <= 0:
            print("New size must be larger than current size.")
            return False

        wood = inv.lookup("Wood")

        if wood is None:
            print("Wood resource not found.")
            return False

        if wood.quantity < costWood:
            print(f"Not enough wood to expand the boat. Required: {costWood}, Available: {wood.quantity}")
            return False

        wood.remove(costWood)
        
        self.size = newSize
        print(f"Boat expanded to size: {self.size}")