import imports as imp
import inventoryLogic as inv
import taskLogic as task


#Items
imp.displayedResources.append(inv.Item("Fishing Rod", 1, breakable=True, breakChance=0.03))
inv.Item("Paddle", 1, breakable=True, breakChance=0.01)

#Resources
inv.Resource("Fish", 0, food = True, hungerScore=100)
inv.Resource("Seaweed", 0, food = True, hungerScore = 8)
imp.displayedResources.append(inv.Resource("Wood", 0))


#Fishing
imp.displayedTasks.append(task.Task(
name="Fishing",
cost={},
neededItems=[inv.lookup("Fishing Rod")],
time=6,
reward= {0.8: ( {}, "You could not catch a fish!"),
        0.95: ( {inv.lookup("Fish"): 1}, "You caught a sardine"),
        0.99: ( {inv.lookup("Fish"): 2}, "You caught a salmon"),
        1.0: ( {inv.lookup("Fish"): 5}, "You caught a tuna")}
))  

#Gather Seaweed
task.Task(name = "Gather Seaweed",
    cost = {},
    neededItems=[],
    time = 2,
    reward = {0.4: ({inv.lookup("Seaweed"): 0}, "You failed to gather seaweed"),
        0.7: ({inv.lookup("Seaweed"): 1}, "You found one piece of seaweed"),
        0.95: ({inv.lookup("Seaweed"): 3}, "You found a large blob of seaweed"),
        1: ({inv.lookup("Seaweed"): 6}, "You found piles of seaweed") })