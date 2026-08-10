import inventoryLogic as inv
import imports as imp

def setBarProgress(value):
    value = max(-100, min(100, value))
    wrapper = imp.document.querySelector("#balance-wrapper")
    bar = imp.document.querySelector("#balance-bar")
    width_percentage = abs(value) / 2
    bar.classList.remove("fill-negative", "fill-positive")
    if value < 0:
        # Move start anchor backward, then expand width forward to the center
        wrapper.style.left = f"{50 - width_percentage}%"
        wrapper.style.width = f"{width_percentage}%"
        bar.classList.add("fill-negative")
    elif value > 0:
        # Lock anchor at the center and expand width rightward
        wrapper.style.left = "50%"
        wrapper.style.width = f"{width_percentage}%"
        bar.classList.add("fill-positive")
    else:
        # Neutral zero point state
        wrapper.style.left = "50%"
        wrapper.style.width = "0%"

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
    all = []

    def __init__(self, name, hunger = 100, task = None):
        self.name = name
        self.hunger = hunger
        self.task = task
        Player.all.append(self)
        self.noFoodMessageDelay = 0

    def eat(self, foodResource):
        if foodResource.quantity > 0:
            self.noFoodMessageDelay = 0 
            foodResource.remove(1)
            self.hunger = min(self.hunger + 100, 100)  # Increase hunger but not above 100
            setBarProgress(self.hunger)
        else:

            if self.noFoodMessageDelay <= 0:
                imp.outputMessage.append(f"{self.name} does not have any {foodResource.name} to eat!")
                self.noFoodMessageDelay = 5
            else:
                self.noFoodMessageDelay -= 1
            
            setBarProgress(self.hunger)

    def hungerFrame(self):
        self.hunger -= 2
        imp.outputMessage.append(f"{self.task.name}")

        if self.hunger <= 0:
            self.eat(inv.lookup("Fish"))
        else:
            setBarProgress(self.hunger)

        if self.hunger <= -100:
            imp.outputMessage.append(f"{self.name} has starved!")

class gameTime:
    def __init__(self):
        self.hours = 0
        self.minutes = 0

    def advance(self, increment):
        self.minutes += increment

        if self.minutes >= 60:
            self.hours += self.minutes // 60
            self.minutes = self.minutes % 60