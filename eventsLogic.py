import taskLogic as task
import inventoryLogic as inv
import imports as imp


class Popup:
    def __init__(self, text, optionTasks, duration = 30):
        self.text = text #Text displayed at top of popup

        self.optionTasks = optionTasks #List of tasks

        self.duration = duration

class Event:
    all = []

    def __init__(self, name, difficulty, minCooldown, screenPopup, cooldown = 60):
        self.name = name
        self.difficulty = difficulty
        self.minCooldown = minCooldown
        self.screenPopup = screenPopup
        self.cooldown = cooldown
        Event.all.append(self)

    async def execute(self):
        #Tasks are in self.screenPopup.optionTaks
        #Text in self.screenPopup.text
        #Duration is in self.screenPopup.duration
        "Input Ezras Complicated Display Code Functions Here!"
        stopEvent(self)
        pass


def eventUpdate(dayNumber):
    for event in Event.all:
        event.cooldown += 1

    if imp.currentEvent is None:
        return

    eligibleEvents = []

    for event in Event.all:
        if event.difficulty <= dayNumber and event.cooldown >= event.minCooldown:
            eligibleEvents.append(event)

    if eligibleEvents is None:
        return

    probability = imp.random.random()

    if probability < 0.01:
        imp.currentEvent = imp.random.choice(eligibleEvents)

        imp.currentEvent.execute()

def stopEvent(event):
    if event is not imp.currentEvent:
        return False

    event.cooldown = 0
    imp.currentEvent = None


#All events down here!
declineTask = task.Task("Decline", {}, [], 0, {})


#Wood floating by event!
woodAcceptTask = task.Task("Paddle to it", {}, [inv.lookup("Paddle")], 0, {
    0.3: ({inv.lookup("Wood"): 0}, "The wood floated away"),
    1: ({inv.lookup("Wood"): 10}, "You managed to salvage ten wood")})

woodPopUp = Popup('You see wood floating by. You may paddle towards it to add it to your inventory.',
                  optionTasks=[woodAcceptTask, declineTask])

woodFloatsBy = Event("Wood Floats By", difficulty=0, minCooldown=90, screenPopup=woodPopUp)

#Another event
