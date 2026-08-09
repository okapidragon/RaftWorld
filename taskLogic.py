import imports as imp
import inventoryLogic as inv



class Task:
    def __init__(self, name, cost, neededItems, time, reward):
        self.name = name
        self.cost = cost #self.cost should be a dictionary of {Resource: amount}
        self.neededItems = neededItems #List of Resource objects
        self.time = time #time in seconds
        self.reward = reward #Dictionary of {Probability: {Resource: amount}}}

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
            print("Not enough resources to execute the task.")
            return False

        for resource, amount in self.cost.items():
            resource.remove(amount)

        imp.time.sleep(self.time)

        for neededItem in self.neededItems:
            breaked = neededItem.tryBreak()
            if breaked:
                return False

        for probability, rewardItems in self.reward.items():
            if imp.random.random() < probability: 
                for rewardItem, amount in rewardItems.items():
                    rewardItem.add(amount) 
                    print(f"Received {rewardItem.name}: {amount} from task {self.name}.")
                return True

#Testing the Task class

wood = inv.Resource("Wood", 100)
fishingRod = inv.Item("Fishing Rod", 1, breakable=True, breakChance=0.1)
fish = inv.Resource("Fish", 1)

fish = Task(
    name="Fishing",
    cost={},
    neededItems=[fishingRod],
    time=1,
    reward={1: {fish: 1}}
)

imp.threading.Thread(target=fish.execute).start()
