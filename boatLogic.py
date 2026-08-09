class Boat:
    def __init__(self, durability, size=(3,6)):
        self.durability = durability
        self.size = size  # Size is a tuple (width, height)

    def expand(self, new_size):
        if new_size[0] > self.size[0] or new_size[1] > self.size[1]:
            self.size = new_size

            

            print(f"Boat expanded to size: {self.size}")
        else:
            print("New size must be larger than current size.")