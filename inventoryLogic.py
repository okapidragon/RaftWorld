import imports as imp

def inventoryUpdate():
    inventory_col = imp.document.querySelector("#inventory-col")
    for resource_line in inventory_col.querySelectorAll(".inventory-resource"):
        resource_line.remove()

    for item in Resource.all:
        item_id = item.name.lower().replace(" ", "-")
        resource_line = imp.document.createElement("p")
        resource_line.style.textAlign = "center"
        resource_line.id = f"{item_id}-count"
        resource_line.className = "inventory-resource"
        resource_line.textContent = f"{item.name}: {item.quantity}"
        inventory_col.appendChild(resource_line)


class Resource:
    all = []
    allFood = []
    
    def __init__(self, name, quantity, food = False, hungerScore = 100):
        self.name = name
        self.quantity = quantity
        Resource.all.append(self)
        inventoryUpdate()

        if food:
            Resource.allFood.append(self)
            self.hungerScore = hungerScore

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
        if self.breakable:
            if imp.random.random() < self.breakChance:
                self.remove(1)
                imp.outputMessage.append(f"{self.name} broke!")

                return True
        return False
        
def lookup(name) -> Resource:
    for resource in Resource.all:
        if resource.name == name:
            return resource
    return None

class CraftingRecipe:
    all = []

    def __init__(self, name, cost, neededItems, result, time = 2):
        self.name = name
        self.cost = cost  # Dictionary of Resource: amount
        self.neededItems = neededItems
        self.time = time #Default time in seconds is 2
        self.result = result  # Dictionary of Resource: amount
        CraftingRecipe.all.append(self)

    def able(self):
        for resource, amount in self.cost.items():
            if resource.quantity < amount:
                return False

        for neededItem in self.neededItems:
            if neededItem.quantity <= 0:
                return False
        
        return True

    async def craft(self):
        if not self.able():
            imp.outputMessage.append("Not enough resources to craft.")
            return False

        for resource, amount in self.cost.items():
            resource.remove(amount)

        await imp.asyncio.sleep(self.time)

        for neededItem in self.neededItems:
            breaked = neededItem.tryBreak()
            if breaked:
                return False

        for resultItem, amount in self.result.items():
            resultItem.add(amount)
    
        imp.outputMessage.append(f"Crafted {self.name}!")

        return True