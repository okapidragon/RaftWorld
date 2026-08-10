import imports as imp
import inventoryLogic as inv
import playerLogic as pl


def initializeSeaweed():
    inv.Resource("Seaweed", 0, food = True, hungerScore = 8)

    Task(name = "Gather Seaweed",
        cost = {},
        neededItems=[],
        time = 2,
        reward = {0.4: ({inv.lookup("Seaweed"): 0}, "You failed to gather seaweed"),
            0.7: ({inv.lookup("Seaweed"): 1}, "You found one piece of seaweed"),
            0.95: ({inv.lookup("Seaweed"): 3}, "You found a large blob of seaweed"),
            1: ({inv.lookup("Seaweed"): 6}, "You found piles of seaweed")
        })

    imp.outputMessage.append("Oh No! Your fishing rod broke. While urgently looking for other food sources, you discover seaweed in the water.")

    taskButtonUpdate()
    inv.inventoryUpdate()

class Task:
    all = []

    def __init__(self, name, cost, neededItems, time, reward):
        self.name = name
        self.cost = cost #self.cost should be a dictionary of {Resource: amount}
        self.neededItems = neededItems #List of Resource objects
        
        self.time = time #time in seconds
        self.reward = reward #Dictionary of {Probability: ({Resource: amount}, dialogue)}} or Function

        if isinstance(reward, dict):
            self.rewardType = "dict"

        if callable(reward):
            self.rewardType = "function"

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

        if (not imp.fishUnlock) and self.name == "Fishing" :
            imp.outputMessage.append('You unlocked fish!')
            inv.inventoryUpdate()
            imp.fishUnlock = True

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
                    imp.outputMessage.append(rewardItems[1])  # Display the dialogue associated with the reward
                    inv.inventoryUpdate()
                    return True
        
        elif self.rewardType == "function":
            if imp.inspect.iscoroutinefunction(self.reward):
                await self.reward()
            else:
                self.reward()

            return True

def lookup(name) -> Task:
    for task in Task.all:
        if task.name == name:
            return task
    return None

async def runTask(selected_task, selected_button):
    selected_button.classList.add("in-progress")
    selected_button.disabled = True

    try:
        await selected_task.execute(pl.Player.all[0])
    finally:
        selected_button.classList.remove("in-progress")
        selected_button.disabled = False

def taskButtonUpdate():
    tasks_col = imp.document.querySelector("#tasks-col")
    for task_button in tasks_col.querySelectorAll(".task-button"):
        task_button.remove()

    for task in Task.all:
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