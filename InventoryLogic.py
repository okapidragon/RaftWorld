class Resource:
    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity

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

    
