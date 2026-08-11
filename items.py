import imports as imp
import inventoryLogic as inv
import taskLogic as task
import eventsLogic as ev


#Items
imp.displayedResources.append(inv.Item("Fishing Rod", 1, breakable=True, breakChance=0.03))
inv.Item("Paddle", 0, breakable=True, breakChance=0.01)

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

#Crafts Here!
task.Task(name = "Craft Paddle",
    cost = {inv.lookup("Wood"): 5},
    neededItems=[],
    time = 2,
    reward = {1: ({inv.lookup("Paddle"): 1}, "Succesful paddle craft!")})



#All events down here!
declineTask = task.Task("Decline", {}, [], 0, {1: ({}, "Declined Event")})


#Wood floating by event!
woodAcceptTask = task.Task("Paddle to it", {}, [inv.lookup("Paddle")], 1, {
    0.3: ({inv.lookup("Wood"): 0}, "The wood floated away"),
    1: ({inv.lookup("Wood"): 10}, "You managed to salvage ten wood")})

woodPopUp = ev.Popup('You see wood floating by. You may paddle towards it to add it to your inventory.', 
optionTasks=[woodAcceptTask, declineTask])

ev.Event("Wood Floats By", difficulty=0, minCooldown=90, screenPopup=woodPopUp)