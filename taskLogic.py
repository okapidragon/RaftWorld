import imports as imp
import inventoryLogic as inv


class Task:
    all = []

    def __init__(self, name, cost, neededItems, time, reward):
        self.name = name
        self.cost = cost #self.cost should be a dictionary of {Resource: amount}
        self.neededItems = neededItems #List of Resource objects
        Task.all.append(self)
        self.time = time #time in seconds
        self.reward = reward #Dictionary of {Probability: ({Resource: amount}, dialogue)}} or Function

        if isinstance(reward, dict):
            self.rewardType = "dict"

        if callable(reward):
            self.rewardType = "function"

    def able(self):
        for resource, amount in self.cost.items():
            if resource.quantity < amount:
                return False

        for neededItem in self.neededItems:
            if neededItem.quantity <= 0:
                return False
        
        return True

    async def execute(self):
        if not self.able():
            imp.outputMessage.append("Not enough resources to execute the task.")
            return False

        for resource, amount in self.cost.items():
            resource.remove(amount)

        await imp.asyncio.sleep(self.time)

        for neededItem in self.neededItems:
            breaked = neededItem.tryBreak()
            if breaked:
                return False

        if self.rewardType == "dict":
            for probability, rewardItems in self.reward.items():
                if imp.random.random() < probability: 
                    for rewardItem, amount in rewardItems[0].items():
                        rewardItem.add(amount) 
                        imp.outputMessage.append(rewardItems[1])  # Display the dialogue associated with the reward
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