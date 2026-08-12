import imports as imp

def inventoryUpdate():
    inventory_col = imp.document.querySelector("#inventory-display")
    for resource_line in inventory_col.querySelectorAll(".inventory-resource"):
        resource_line.remove()

    for item in imp.displayedResources:
        item_id = item.name.lower().replace(" ", "-")
        resource_line = imp.document.createElement("p")
        resource_line.style.textAlign = "center"
        resource_line.id = f"{item_id}-count"
        resource_line.className = "inventory-resource"
        resource_line.textContent = f"{item.name}: {item.quantity}"
        crafts_col = inventory_col.querySelector("#crafts-col")
        if crafts_col is not None:
            inventory_col.insertBefore(resource_line, crafts_col)
        else:
            inventory_col.appendChild(resource_line)


class Resource:
    all = []
    allFood = []
    
    def __init__(self, name, quantity, food = False, hungerScore = 100, eatQuantity = 1):
        self.name = name
        self.quantity = quantity
        Resource.all.append(self)
        inventoryUpdate()

        if food:
            Resource.allFood.append(self)
            self.hungerScore = hungerScore
            self.eatQuantity = eatQuantity

    def add(self, amount):
        self.quantity += amount
        inventoryUpdate()

    def remove(self, amount):
        if amount <= self.quantity:
            self.quantity -= amount
            inventoryUpdate()
            return True
        else:
            imp.outputMessage.append(f"Not enough {self.name} in inventory to remove {amount}. Current quantity: {self.quantity}")

    def __str__(self):
        return f"{self.name}: {self.quantity}"


class Item(Resource):
    def __init__(self, name, quantity, breakable=False, breakChance=0.0):
        super().__init__(name, quantity)
        self.breakable = breakable
        self.breakChance = breakChance

    def tryBreak(self):
        if (self.breakable) and (imp.random.random() < self.breakChance):
            self.remove(1)
            imp.outputMessage.append(f"Oh No! {self.name} broke.", color = "Red")

            return True
        return False
        
def lookup(name) -> Resource:
    for resource in Resource.all:
        if resource.name == name:
            return resource
    return None