import imports as imp
import inventoryLogic as inv


def initializeSeaweed():
    imp.displayedResources.append(inv.lookup("Seaweed"))
    imp.displayedTasks.append(lookup("Gather Seaweed"))

    imp.outputMessage.append("While urgently looking for other food sources, you discover seaweed in the water.", color = "#50C878")

    if not (inv.lookup("Fish") in imp.displayedResources):
        imp.displayedResources.append(inv.lookup("Fish"))

    taskButtonUpdate()
    inv.inventoryUpdate()

class Task:
    all = []
    allCraft = []

    def __init__(self, name, cost, neededItems, time, reward, inputs = None, craft = False):
        self.name = name
        self.cost = cost #self.cost should be a dictionary of {Resource: amount}
        self.neededItems = neededItems #List of Resource objects
        
        self.time = time #time in seconds
        self.reward = reward #Dictionary of {Probability: ({Resource: amount}, dialogue)}} or Function
        self.inputs = inputs

        if isinstance(reward, dict):
            self.rewardType = "dict"

        if callable(reward):
            self.rewardType = "function"

        if craft:
            Task.allCraft.append(self)

        Task.all.append(self)

    def able(self):
        for resource, amount in self.cost.items():
            if resource.quantity < amount:
                return False

        for neededItem in self.neededItems:
            if neededItem.quantity <= 0:
                return False
        
        return True

    async def execute(self, player):
        if player.task is not None:
            imp.outputMessage.append(f"Player is already doing {player.task.name}.")
            return False

        player.task = self

        if not self.able():
            imp.outputMessage.append("Not enough resources to execute the task.")
            player.task = None
            return False

        for resource, amount in self.cost.items():
            resource.remove(amount)

        await imp.asyncio.sleep(self.time)

        for neededItem in self.neededItems:
            breaked = neededItem.tryBreak()
            if breaked:
                if neededItem.name == "Fishing Rod" and not imp.seaweedUnlock:
                    player.task = None
                    initializeSeaweed()
                    return False

                player.task = None
                return False

        player.task = None

        if self.rewardType == "dict":
            for probability, rewardItems in self.reward.items():
                if imp.random.random() < probability: 
                    for rewardItem, amount in rewardItems[0].items():
                        rewardItem.add(amount) 
                        if not (rewardItem in imp.displayedResources):
                            imp.displayedResources.append(rewardItem)

                    imp.outputMessage.append(rewardItems[1])  # Display the dialogue associated with the reward
                    inv.inventoryUpdate()
                    return True
        
        elif self.rewardType == "function":
            if self.inputs is not None:
                self.reward(self.inputs)

            elif imp.inspect.iscoroutinefunction(self.reward):
                await self.reward()
            else:
                self.reward()

            return True

        return True

def lookup(name) -> Task:
    for task in Task.all:
        if task.name == name:
            return task
    return None

async def runTask(selected_task, selected_button):
    import playerLogic as pl

    selected_button.classList.add("in-progress")
    selected_button.disabled = True

    try:
        happened = await selected_task.execute(pl.Player.all[0])
    finally:
        selected_button.classList.remove("in-progress")
        selected_button.disabled = False
    return happened

def taskButtonUpdate():
    tasks_col = imp.document.querySelector("#tasks-col")
    for task_button in tasks_col.querySelectorAll(".task-button"):
        task_button.remove()

    for task in imp.displayedTasks:
        task_id = task.name.lower().replace(" ", "-")
        task_button = imp.document.createElement("button")
        task_button.style.display = "block"
        task_button.style.margin = "0 auto 20px"
        task_button.id = f"{task_id}-button"
        task_button.className = "task-button"
        task_button.textContent = task.name
        task_button.onclick = (
            lambda event, selected_task=task, selected_button=task_button:
            imp.asyncio.create_task(
                runTask(selected_task, selected_button)
            )
        )
        tasks_col.appendChild(task_button)
        tasks_col.appendChild(task_button)
        tasks_col.appendChild(imp.document.createElement("br"))