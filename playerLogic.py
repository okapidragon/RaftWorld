import inventoryLogic as inv
import imports as imp
import taskLogic as task
import items as item

def setHungerBarProgress(value):
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

def setHealthBarProgress(value):
    value = min(100, max(0, value))
    health_bar = imp.document.querySelector("#health-bar")
    health_bar.style.width = f"{value}%"
    

def displayBoatSize(boat):
    size_display = imp.document.querySelector("#boat-size")
    size_display.textContent = f"Boat size: {boat.size[0]} x {boat.size[1]}"

def displayTime(current_time):
    timeText = f"{current_time.hours:02d}:{current_time.minutes:02d}, Day {current_time.days}"
    time_line = imp.document.querySelector("#time-display")
    time_line.textContent = f"Time: {timeText}"

def setDecayBarProgress(value):
    value = min(100, max(0, value))
    value = 100 - value
    decay_bar = imp.document.querySelector("#decay-bar")
    decay_bar.style.width = f"{value}%"

async def resizeBoat(event=None):
    width_input = imp.document.querySelector("#boat-width")
    height_input = imp.document.querySelector("#boat-height")

    width = (width_input.value)
    height = (height_input.value)

    try:
        width = int(width)
        height = int(height)
    except ValueError:
        imp.outputMessage.append("The side lengths must be integers")
        return
    

    newSize = (width, height)

    if Player.all[0].task is not None:
        imp.outputMessage.append(f"Player is already doing {Player.all[0].task.name}.")
        return

    ogWidth = Boat.all[0].size[0]
    ogHeight = Boat.all[0].size[1]

    if width == ogWidth and height == ogHeight:
        imp.outputMessage.append("Boat is already that size")
        return

    addedArea = width * height - ogHeight * ogWidth

    if addedArea > inv.lookup("Wood").quantity:
        imp.outputMessage.append("Not enough wood")
        return

    if width < 5 or height < 5:
        imp.outputMessage.append("Minimum side of 5 wood")
        return

    

    boatSizeChange = task.Task(
        name = "Change Boat Size",
        cost = {},
        neededItems=[],
        time = 3,
        reward = Boat.all[0].changeSize,
        inputs = newSize)

    task.Task.all.remove(boatSizeChange)

    resize_button.classList.add("in-progress")
    resize_button.disabled = True

    try:
        await boatSizeChange.execute(Player.all[0])
    finally:
        resize_button.classList.remove("in-progress")
        resize_button.disabled = False
    





resize_button = imp.document.querySelector("#resize-boat-button")
resize_button.onclick = resizeBoat

class Boat:
    all = []

    def __init__(self, durability, size, decay = 0, decaySpeed = 0.1):
        self.durability = durability
        self.size = size  # Size is a tuple (width, height)
        self.decay = decay
        self.decaySpeed = decaySpeed
        Boat.all.append(self)

    def changeSize(self, newSize):
        newSize = (int(newSize[0]), int(newSize[1]))
        
        addArea = (newSize[0] * newSize[1]) - (self.size[0] * self.size[1])

        self.size = newSize

        sizeText = f"{self.size[0]}x{self.size[1]}"

        displayBoatSize(Boat.all[0])

        if addArea > 0:
            inv.lookup("Wood").remove(addArea)
            imp.outputMessage.append(f"Boat increased to size {sizeText}. Used {addArea} wood.")
        elif addArea < 0:
            inv.lookup("Wood").add(-addArea)
            imp.outputMessage.append(f"Boat decreased to size {sizeText}. Salvaged {-addArea} wood.") 

        if not (inv.lookup("Wood") in imp.displayedResources):
            imp.displayedResources.append(inv.lookup("Wood"))
            imp.asyncio.create_task(task.craftButtonUpdate())

    def decayFrame(self):
        if imp.boatDecay:
            self.decaySpeed = max(0, self.decaySpeed)
            self.decaySpeed += 0.015
            self.decay += self.decaySpeed

        setDecayBarProgress(self.decay)

class Player:
    all = []

    def __init__(self, name, hunger = 100, task = None, health = 100):
        self.name = name
        self.hunger = hunger
        self.task = task
        self.health = health
        Player.all.append(self)
        self.noFoodMessageDelay = 0

    def eat(self, foodResource):
        self.noFoodMessageDelay = 0 

        quantity = min(foodResource.eatQuantity, foodResource.quantity)

        foodResource.remove(quantity)
        self.hunger = min(self.hunger + foodResource.hungerScore * quantity, 100)  # Increase hunger but not above 100
        setHungerBarProgress(self.hunger)

        if quantity == 1:
            imp.outputMessage.append(f"A {foodResource.name} was eaten.")
        else:
            imp.outputMessage.append(f"{quantity} {foodResource.name} were eaten.")
        inv.inventoryUpdate()

    def hungerFrame(self):

        if (not (inv.lookup("Fish") in imp.displayedResources) ) and imp.countdown <= 30:
            setHungerBarProgress(self.hunger)
            imp.countdown += 1
            return

        if (not (inv.lookup("Spear") in imp.displayedCrafts) )and imp.metalUnlock:
            imp.displayedCrafts.append(task.lookup("Craft Spear"))
            imp.displayedCrafts.append(task.lookup("Craft Anchor"))
            task.craftButtonUpdate()


        self.hunger -= 1.3
        setHungerBarProgress(self.hunger)

        if self.hunger <= 0:
            for food in inv.Resource.allFood:
                if food.quantity > 0:
                    self.eat(food)
                    return

            if self.noFoodMessageDelay <= 0:
                imp.outputMessage.append(f"{self.name} has no food to eat", color = "Red")
                self.noFoodMessageDelay = 5
            else:
                self.noFoodMessageDelay -= 1
            
            setHungerBarProgress(self.hunger)
        else:
            self.health += 1
            setHealthBarProgress(self.health)
            setHungerBarProgress(self.hunger)

        if self.hunger <= -100:
            imp.outputMessage.append(f"{self.name} has starved!", color = "Red")
            self.health -= 2.5
            setHealthBarProgress(self.health)

    def setHealth(self):
        setHealthBarProgress(self.health)

    
class gameTime:
    all = []

    def __init__(self):
        self.hours = 0
        self.minutes = 0
        self.days = 1
        gameTime.all.append(self)

    def advance(self, increment):
        self.minutes += increment

        if self.minutes >= 60:
            self.hours += self.minutes // 60
            self.minutes = self.minutes % 60

        if self.hours >= 24:
            self.days += self.hours // 24
            self.hours = self.hours % 24


