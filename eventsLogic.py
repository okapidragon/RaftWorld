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
        imp.currentEvent = self

        events_column = imp.document.querySelector("#events-col")
        
        message_line = imp.document.createElement("p")
        message_line.className = "event-message"
        message_line.style.textAlign = "center"
        message_line.textContent = self.screenPopup.text
        events_column.appendChild(message_line)

        self.timerTask = imp.asyncio.create_task(self.eventTimer())

        for taskItem in self.screenPopup.optionTasks:
            task_id = taskItem.name.lower().replace(" ", "-")
            task_button = imp.document.createElement("button")
            task_button.style.display = "block"
            task_button.style.margin = "0 auto 20px"
            task_button.id = f"{task_id}-button"
            task_button.className = "event-button"
            task_button.textContent = taskItem.name
            task_button.onclick = (
                lambda event, selected_task=taskItem, selected_button=task_button:
                imp.asyncio.create_task(
                self.chooseOption(selected_task, selected_button)
            )
            )
            events_column.appendChild(task_button)

    async def eventTimer(self):
        events_column = imp.document.querySelector("#events-col")

        timer_div = imp.document.createElement("div")
        timer_div.className = "event-timer"
        timer_div.style.textAlign = "center"
        events_column.appendChild(timer_div)        

        for remaining in range(self.screenPopup.duration, 0, -1):
            timer_div.innerHTML = "" 
            timer = imp.document.createElement("p")
            timer.className = "timer"
            timer.style.textAlign = "center"
            timer.textContent = f"Time remaining: {remaining}"
            timer_div.appendChild(timer)
            await imp.asyncio.sleep(1)

        # Time ran out
        if imp.currentEvent is self:
            imp.outputMessage.append("You could not reach it in time.")
            stopEvent(self)

    async def chooseOption(self, selected_task, selected_button):
    # Make sure the event hasn't already timed out
        if imp.currentEvent is not self:
            return
        
        self.timerTask.cancel()

        happened = await task.runTask(selected_task, selected_button)

        if happened:
            stopEvent(self)

        


def eventUpdate(dayNumber):
    for event in Event.all:
        event.cooldown += 1

    if imp.currentEvent is not None:
        return

    eligibleEvents = []

    for event in Event.all:
        if event.difficulty <= dayNumber and event.cooldown >= event.minCooldown:
            eligibleEvents.append(event)

    if len(eligibleEvents) == 0:
        return

    probability = imp.random.random()

    if probability < 0.01:
        imp.currentEvent = imp.random.choice(eligibleEvents)

        imp.asyncio.create_task(imp.currentEvent.execute())

def stopEvent(event):
    if event is not imp.currentEvent:
        return False
    
    events_column = imp.document.querySelector("#events-col")
    for event_button in events_column.querySelectorAll(".event-button"):
        event_button.remove()

    for event_message in events_column.querySelectorAll(".event-message"):
        event_message.remove()

    for event_timer in events_column.querySelectorAll(".event-timer"):
        event_timer.remove()

    event.cooldown = 0
    imp.currentEvent = None

    if not imp.boatUnlock and event.name == "Wood Floats By":
        imp.showSomething("#boat-col")
        imp.outputMessage.append("While pondering a way to get a paddle. You notice that you can take apart your raft, your only life supply. Be Careful!")
        imp.boatUnlock = True

#All events down here!
declineTask = task.Task("Decline", {}, [], 0, {1: ({}, "Declined Event")})


#Wood floating by event!
woodAcceptTask = task.Task("Paddle to it", {}, [inv.lookup("Paddle")], 1, {
    0.3: ({inv.lookup("Wood"): 0}, "The wood floated away"),
    1: ({inv.lookup("Wood"): 10}, "You managed to salvage ten wood")})

woodPopUp = Popup('You see wood floating by. You may paddle towards it to add it to your inventory.',
                  optionTasks=[woodAcceptTask, declineTask])

woodFloatsBy = Event("Wood Floats By", difficulty=0, minCooldown=90, screenPopup=woodPopUp)
