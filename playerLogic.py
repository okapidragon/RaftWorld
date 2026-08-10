import inventoryLogic as inv
import imports as imp
import taskLogic as task

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

def displayBoatSize(boat):
    size_display = imp.document.querySelector("#boat-size")
    size_display.textContent = f"Boat size: {boat.size[0]} x {boat.size[1]}"

def resizeBoat(event=None):
    width_input = imp.document.querySelector("#boat-width")
    height_input = imp.document.querySelector("#boat-height")

    width = int(width_input.value)
    height = int(height_input.value)
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

    boatSizeChange = task.Task(
        name = "Change Boat Size",
        cost = {},
        neededItems=[],
        time = 5,
        reward = Boat.all[0].changeSize,
        inputs = newSize)

    task.Task.all.remove(boatSizeChange)

    imp.asyncio.create_task(boatSizeChange.execute(Player.all[0]))




resize_button = imp.document.querySelector("#resize-boat-button")
resize_button.onclick = resizeBoat

class Boat:
    all = []

    def __init__(self, durability, size):
        self.durability = durability
        self.size = size  # Size is a tuple (width, height)
        Boat.all.append(self)

    def changeSize(self, newSize):
        try:
            newSize = (int(newSize[0]), int(newSize[1]))
        except ValueError:
            imp.outputMessage.append("The side lengths must be integers")
            return

        addArea = (newSize[0] * newSize[1]) - (self.size[0] * self.size[1])

        #Change minimum area to 25 size per person
        if (newSize[0] < 5) or (newSize[1] < 5):
            imp.outputMessage.append("The minimum size per side is 5 wood.")
            return False

        self.size = newSize

        sizeText = f"{self.size[0]}x{self.size[1]}"

        displayBoatSize(Boat.all[0])

        if addArea > 0:
            inv.lookup("Wood").remove(addArea)
            imp.outputMessage.append(f"Boat increased to size {sizeText}. Used {addArea} wood.")
        elif addArea < 0:
            inv.lookup("Wood").add(-addArea)
            imp.outputMessage.append(f"Boat decreased to size {sizeText}. Salvaged {-addArea} wood.") 

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
            self.hunger = min(self.hunger + foodResource.hungerScore, 100)  # Increase hunger but not above 100
            setBarProgress(self.hunger)
            imp.outputMessage.append(f"{foodResource.name} was eaten.")
            inv.inventoryUpdate()

    def hungerFrame(self):
        if not imp.fishUnlock:
            setBarProgress(self.hunger)
            return

        self.hunger -= 2

        if self.hunger <= 0:
            for food in inv.Resource.allFood:
                if food.quantity > 0:
                    self.eat(food)
                    return

            if self.noFoodMessageDelay <= 0:
                imp.outputMessage.append(f"{self.name} has no food to eat")
                self.noFoodMessageDelay = 5
            else:
                self.noFoodMessageDelay -= 1
            
            setBarProgress(self.hunger)
        else:
            setBarProgress(self.hunger)

        if self.hunger <= -100:
            imp.outputMessage.append(f"{self.name} has starved!")


def displayTime(current_time):
    timeText = f"{current_time.hours:02d}:{current_time.minutes:02d}, Day {current_time.days}"
    time_line = imp.document.querySelector("#time-display")
    time_line.textContent = f"Time: {timeText}"

class gameTime:
    all = []

    def __init__(self):
        self.hours = 0
        self.minutes = 0
        self.days = 0
        gameTime.all.append(self)

    def advance(self, increment):
        self.minutes += increment

        if self.minutes >= 60:
            self.hours += self.minutes // 60
            self.minutes = self.minutes % 60

        if self.hours >= 24:
            self.days += self.hours // 24
            self.hours = self.hours % 24
