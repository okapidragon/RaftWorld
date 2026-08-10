import imports as imp
import inventoryLogic as inv


class Task:
    def __init__(self, name, cost, neededItems, time, reward):
        self.name = name
        self.cost = cost #self.cost should be a dictionary of {Resource: amount}
        self.neededItems = neededItems #List of Resource objects
        self.time = time #time in seconds
        self.reward = reward #Dictionary of {Probability: {Resource: amount}}} or Function

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

    def execute(self):
        if not self.able():
            imp.outputMessage += "Not enough resources to execute the task."
            return False

        for resource, amount in self.cost.items():
            resource.remove(amount)

        imp.time.sleep(self.time)

        for neededItem in self.neededItems:
            breaked = neededItem.tryBreak()
            if breaked:
                return False

        if self.rewardType == "dict":
            for probability, rewardItems in self.reward.items():
                if imp.random.random() < probability: 
                    for rewardItem, amount in rewardItems.items():
                        rewardItem.add(amount) 
                        imp.outputMessage += f"Received {rewardItem.name}: {amount} from task {self.name}."
                    return True
        elif self.rewardType == "function":
            self.reward()

            return True