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

    def __init__(self, name, minCooldown, screenPopup, weightFunc, cooldown = 60, automaticFunc = None, timer = True, multipleTasks = False, stopFunc = None, randomItems = False):
        self.name = name
        self.minCooldown = minCooldown
        self.screenPopup = screenPopup
        self.cooldown = cooldown
        self.weightFunc = weightFunc
        self.timer = timer
        self.multipleTasks = multipleTasks
        self.stopFunc = stopFunc
        self.randomItems = randomItems

        if not callable(weightFunc):
            imp.outputMessage.append(f"{self.name} event weightFunc is not callable!")

        Event.all.append(self)
        self.automaticFunc = automaticFunc #Cannot wait during!

    #Execute finishes but eventTimer conitnues and chooseOption runs on button click.
    async def execute(self):
        imp.eventNumber += 1
        imp.showSomething("#events-div")
        imp.currentEvent = self

        if self.automaticFunc is not None:
            if imp.inspect.iscoroutinefunction(self.automaticFunc):
                imp.asyncio.create_task(self.automaticFunc())
            else:
                self.automaticFunc()
        
        events_column = imp.document.querySelector("#events-div")
        
        message_line = imp.document.createElement("p")
        message_line.className = "event-message"
        message_line.style.textAlign = "center"
        message_line.textContent = self.screenPopup.text
        events_column.appendChild(message_line)

        self.timerTask = imp.asyncio.create_task(self.eventTimer())

        newOptions = self.screenPopup.optionTasks.copy()

        if self.randomItems is not False:
            indices = imp.random.sample(range(len(newOptions)), self.randomItems)
            indices.sort()
            newOptions = [self.screenPopup.optionTasks[i] for i in indices]

        for taskItem in newOptions:
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
            if taskItem.cost:
                for item in taskItem.cost.keys():
                    cost_line = imp.document.createElement("p")
                    cost_line.style.textAlign = "center"
                    cost_line.id = f"{item}-button"
                    cost_line.textContent = f"Cost: {taskItem.cost[item]} {item.name}"
                    events_column.appendChild(cost_line)



    async def eventTimer(self):
        try:
            events_column = imp.document.querySelector("#events-div")

            if self.timer:
                timer_div = imp.document.createElement("div")
                timer_div.className = "event-timer"
                timer_div.style.textAlign = "center"
                events_column.appendChild(timer_div)        

            for remaining in range(self.screenPopup.duration, 0, -1):
                if self.timer:
                    timer_div.innerHTML = "" 
                    timer = imp.document.createElement("p")
                    timer.className = "timer"
                    timer.style.textAlign = "center"
                    timer.textContent = f"Time remaining: {remaining}"
                    timer_div.appendChild(timer)
                await imp.pause_aware_sleep(1)

            # Time ran out
            if imp.currentEvent is self:
                imp.outputMessage.append("The event is now over!")

                if self.stopFunc is not None:
                    self.stopFunc()

                imp.asyncio.create_task(stopEvent(self))
        except:
            pass

                

    async def chooseOption(self, selected_task, selected_button):
        try:
            if imp.currentEvent is not self:
                return

            happened = await task.runTask(selected_task, selected_button)

            if happened and not self.multipleTasks:
                self.timerTask.cancel()
                imp.asyncio.create_task(stopEvent(self))
        except:
            pass

            


def eventUpdate(dayNumber):
    for event in Event.all:
        event.cooldown += 1

    if imp.currentEvent is not None:
        return

    imp.timeSinceEvent += 1

    eligibleEvents = []

    for event in Event.all:
        if  event.cooldown >= event.minCooldown:
            eligibleEvents.append(event)

    if len(eligibleEvents) == 0:
        return

    probability = imp.random.random()

    if probability < imp.timeSinceEvent * 0.001:
        weightedEventDict = {}

        for eventItem in eligibleEvents:
            weightedEventDict[eventItem] = eventItem.weightFunc()

        if sum(weightedEventDict.values()) <= 0:
            return

        totalWeight = sum(weightedEventDict.values())

        normEventDict = {}

        for eventItem, weight in weightedEventDict.items():
            lastValue = next(reversed(normEventDict.values()), 0)

            normEventDict[eventItem] = lastValue + (weight / totalWeight)

        randomChosen = imp.random.random()

        for eventItem, probability in normEventDict.items():
            if randomChosen < probability:
                imp.currentEvent = eventItem
                break
            


        imp.timeSinceEvent = 0

        imp.asyncio.create_task(imp.currentEvent.execute())

async def stopEvent(event):
    try:
        if event is not imp.currentEvent:
            return False

        imp.hideSomething("#events-div")

        
        events_column = imp.document.querySelector("#events-div")
        events_column.innerHTML = ""
        event.cooldown = 0
        imp.currentEvent = None

        if not imp.boatUnlock:
            await imp.pause_aware_sleep(3)

            imp.showSomething("#boat-div")
            imp.outputMessage.append("While pondering a way to get a paddle. You notice that you can take apart your raft, your only life supply. Be Careful!", color = "#50C878")
            imp.boatUnlock = True
            paddle_craft = task.lookup("Craft Paddle")
            if paddle_craft is not None:
                imp.displayedCrafts.append(paddle_craft)

            await imp.pause_aware_sleep(3)
            
            task.craftButtonUpdate()

        boat_button = imp.document.querySelector("#resize-boat-button")
        boat_button.disabled = False
    except:
        pass

def lookup(name):
    for eventItem in Event.all:
        if eventItem.name == name:
            return eventItem

    imp.outputMessage.append(f"{name} not found as an event.")