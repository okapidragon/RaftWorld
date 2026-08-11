import imports as imp
import inventoryLogic as inv
import taskLogic as task
import eventsLogic as ev
import playerLogic as pl


#Items
imp.displayedResources.append(inv.Item("Fishing Rod", 1, breakable=True, breakChance=0.07))
inv.Item("Paddle", 0, breakable=True, breakChance=0.01)

#Resources
inv.Resource("Fish", 0, food = True, hungerScore=100)
inv.Resource("Seaweed", 0, food = True, hungerScore = 8, eatQuantity = 5)
inv.Resource("Fishing Reel", 0)
imp.displayedResources.append(inv.Resource("Wood", 0))


#Fishing
imp.displayedTasks.append(task.Task(
name="Fishing",
cost={},
neededItems=[inv.lookup("Fishing Rod")],
time=7,
reward= {0.8: ( {inv.lookup("Fish"): 0}, "You could not catch a fish!"),
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
imp.displayedCrafts.append(
task.Task(name = "Craft Paddle",
    cost = {inv.lookup("Wood"): 5},
    neededItems=[],
    time = 2,
    reward = {1: ({inv.lookup("Paddle"): 1}, "Succesful paddle craft!")}, craft=True)
)
task.Task(name = "Craft Fishing Rod",
    cost = {inv.lookup("Wood"): 4, inv.lookup("Fishing Reel"): 1},
    neededItems=[],
    time = 3,
    reward = {1: ({inv.lookup("Fishing Rod"): 1}, "Succesful fishing rod craft!")}, craft=True
)

#All events down here!
declineTask = task.Task("Decline", {}, [], 0, {1: ({}, "Declined Event")})


#Wood floating by event!
woodAcceptTask = task.Task("Paddle to it", {}, [inv.lookup("Paddle")], 1, {
    0.3: ({inv.lookup("Wood"): 0}, "The wood floated away"),
    1: ({inv.lookup("Wood"): 10}, "You managed to salvage ten wood")})

woodPopUp = ev.Popup('You see wood floating by. You may paddle towards it to add it to your inventory.', 
optionTasks=[woodAcceptTask, declineTask])

ev.Event("Wood Floats By", difficulty=0, minCooldown=20, screenPopup=woodPopUp, weight = 4)

#String Floats By
stringAcceptTask = task.Task("Paddle to it", {}, [inv.lookup("Paddle")], 1, { 
    0.3: ({inv.lookup("Fishing Reel"): 0}, "The fishing reel floated away"),
    1: ({inv.lookup("Fishing Reel"): 1}, "You managed to salvage one fishing reel")})

stringPopUp = ev.Popup('You see a fishing reel floating by. You may paddle towards it to add it to your inventory.',
optionTasks=[stringAcceptTask, declineTask])

ev.Event("String Floats By", difficulty=1, minCooldown=20, screenPopup=stringPopUp, weight = 2)

#Fishing cut yourself
def cut():
    pl.Player.all[0].health -= 25
    imp.outputMessage.append("You cut yourself on the fishing rod and lost 25 health.", color = "Red")

def cutCondition():
    return (inv.lookup("Fishing Rod").quantity > 0)

stringPopUp = ev.Popup('You cut yourself on the fishing rod and lost 25 health',[], duration = 15)

ev.Event("Fishing Cut", difficulty = 1, minCooldown = 40, screenPopup=stringPopUp, condition=cutCondition, automaticFunc=cut())



