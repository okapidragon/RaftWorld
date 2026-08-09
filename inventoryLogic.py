import imports as imp

class Resource:
    all = []

    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity
        Resource.all.append(self)

    def add(self, amount):
        self.quantity += amount

    def remove(self, amount):
        if amount <= self.quantity:
            self.quantity -= amount
            return True
        else:
            raise ValueError(f"Not enough {self.name} in inventory to remove {amount}. Current quantity: {self.quantity}")

    def __str__(self):
        return f"{self.name}: {self.quantity}"


class Item(Resource):
    def __init__(self, name, quantity, breakable=False, breakChance=0.0):
        super().__init__(name, quantity)
        self.breakable = breakable
        self.breakChance = breakChance

    def tryBreak(self):
        if self.breakable:
            if imp.random.random() < self.breakChance:
                self.remove(1)
                print(f"{self.name} broke!")
                return True
        return False
        
def lookup(name):
    for resource in Resource.all:
        if resource.name == name:
            return resource
    return None

