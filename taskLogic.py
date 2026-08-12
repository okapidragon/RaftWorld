import imports as imp
import inventoryLogic as inv


def initializeSeaweed():
    imp.displayedResources.append(inv.lookup("Seaweed"))
    imp.displayedTasks.append(lookup("Gather Seaweed"))

    imp.outputMessage.append("While urgently looking for other food sources, you discover seaweed in the water.", color = "#50C878")

    if not (inv.lookup("Fish") in imp.displayedResources):
        imp.displayedResources.append(inv.lookup("Fish"))

    imp.outputMessage.append("You may now craft a fishing rod", color = "#50C878")
    imp.displayedCrafts.append(lookup("Craft Fishing Rod"))

    imp.asyncio.create_Task.craftButtonUpdate()
    taskButtonUpdate()
    inv.inventoryUpdate()

#Fishing cut yourself
def cut(player, taskName):
    player.health -= 15
    imp.outputMessage.append(f"You cut yourself while {taskName}.", color = "Red")

def swimTrouble(player, taskName):
    player.health -= 12
    imp.outputMessage.append(f"You spent too long in the wat {taskName}.", color = "Red")

class Task:
    all = []
    allCraft = []

    def __init__(self, name, cost, neededItems, time, reward, inputs = None, craft = False, cutChance = 0, swimTroubleChance = 0):
        self.name = name
        self.cost = cost #self.cost should be a dictionary of {Resource: amount}
        self.neededItems = neededItems #List of Resource objects

        self.time = time #time in seconds
        self.reward = reward #Dictionary of {Probability: ({Resource: amount}, dialogue)}} or Function
        self.inputs = inputs
        self.cutChance = cutChance
        self.swimTroubleChance = swimTroubleChance

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
                imp.outputMessage.append(f"Need {resource.quantity - amount} more {resource.name}")
                return False

        for neededItem in self.neededItems:
            if neededItem.quantity <= 0:
                imp.outputMessage.append(f"Need a {neededItem.name}")
                return False
        
        return True

    async def execute(self, player):
        if player.task is not None:
            imp.outputMessage.append(f"Player is already doing {player.task.name}.")
            return False

        player.task = self

        if not self.able():
            player.task = None
            return False

        for resource, amount in self.cost.items():
            resource.remove(amount)

        await imp.asyncio.sleep(self.time)

        if imp.random.random() < self.cutChance:
            cut(player, self.name)

        if imp.random.random() < self.swimTroubleChance:
            swimTrouble(player, self.name)

        for neededItem in self.neededItems:
            breaked = neededItem.tryBreak()
            if breaked:
                if neededItem.name == "Fishing Rod" and not imp.seaweedUnlock:
                    initializeSeaweed()

                player.task = None
                return True

        player.task = None

        if self.rewardType == "dict":
            for probability, rewardItems in self.reward.items():
                if imp.random.random() < probability: 
                    for rewardItem, amount in rewardItems[0].items():
                        rewardItem.add(amount) 
                        if not (rewardItem in imp.displayedResources):
                            imp.displayedResources.append(rewardItem)
                            imp.asyncio.create_Task.craftButtonUpdate()

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
    tasks_col = imp.document.querySelector("#tasks-area")
    for task_button in tasks_col.querySelectorAll(".task-button"):
        task_button.remove()

    for task in imp.displayedTasks:
        task_id = task.name.lower().replace(" ", "-")
        task_button = imp.document.createElement("button")
        task_button.style.display = "block"
        task_button.style.margin = "0 auto 8px"
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

        if task.cost:
            cost_line = imp.document.createElement("p")
            cost_line.style.textAlign = "center"
            cost_line.style.margin = "4px 0"
            cost_line.innerHTML = f"Resources needed: {', '.join([f'{amount} {resource.name}' for resource, amount in task.cost.items()])}"
            tasks_col.appendChild(cost_line)

async def craftButtonUpdate():
    if imp.craftingShown:
        craft_col = imp.document.querySelector("#crafts-col")
        craft_col.innerHTML = ""

        if not imp.displayedCrafts:
            craft_col.style.display = "none"
            return

        craft_col.style.display = "block"
        craft_header = imp.document.createElement("h3")
        craft_header.textContent = "Crafting"
        craft_header.style.textAlign = "center"
        craft_header.style.width = "100%"
        craft_header.style.margin = "0 0 16px"
        craft_col.appendChild(craft_header)

        for craft in imp.displayedCrafts:
            if craft is None:
                continue
            craft_id = craft.name.lower().replace(" ", "-")
            craft_button = imp.document.createElement("button")
            craft_button.style.display = "block"
            craft_button.style.margin = "0 auto 8px"
            craft_button.id = f"{craft_id}-button"
            craft_button.className = "craft-button"
            craft_button.textContent = craft.name
            craft_cost = imp.document.createElement("p")
            craft_cost.style.textAlign = "center"
            craft_cost.style.margin = "4px 0"
            craft_cost.innerHTML = f"Resources needed: {', '.join([f'{amount} {resource.name}' for resource, amount in craft.cost.items()])}"
            craft_button.onclick = (
                lambda event, selected_task=craft, selected_button=craft_button:
                imp.asyncio.create_task(
                    runTask(selected_task, selected_button)
                )
            )
            craft_col.appendChild(craft_button)
            craft_col.appendChild(craft_cost)
        else:
            imp.displayedCrafts = True
            await imp.asyncio.sleep(3)
            craft_col = imp.document.querySelector("#crafts-col")
            craft_col.innerHTML = ""
    
            if not imp.displayedCrafts:
                craft_col.style.display = "none"
                return
    
            craft_col.style.display = "block"
            craft_header = imp.document.createElement("h3")
            craft_header.textContent = "Crafting"
            craft_header.style.textAlign = "center"
            craft_header.style.width = "100%"
            craft_header.style.margin = "0 0 16px"
            craft_col.appendChild(craft_header)
    
            for craft in imp.displayedCrafts:
                if craft is None:
                    continue
                craft_id = craft.name.lower().replace(" ", "-")
                craft_button = imp.document.createElement("button")
                craft_button.style.display = "block"
                craft_button.style.margin = "0 auto 20px"
                craft_button.id = f"{craft_id}-button"
                craft_button.className = "craft-button"
                craft_button.textContent = craft.name
                craft_cost = imp.document.createElement("p")
                craft_cost.style.textAlign = "center"
                craft_cost.innerHTML = f"Resources needed: {', '.join([f'{amount} {resource.name}' for resource, amount in craft.cost.items()])}"
                craft_button.onclick = (
                    lambda event, selected_task=craft, selected_button=craft_button:
                    imp.asyncio.create_task(
                        runTask(selected_task, selected_button)
                    )
                )
                craft_col.appendChild(craft_button)
                craft_col.appendChild(craft_cost)
                craft_col.appendChild(imp.document.createElement("br"))

def locationUpdate(place):
    location_col = imp.document.querySelector("#location")
    location_col.innerHTML = f"<p style=\"text-align: center;\">Location: {place}</p>"