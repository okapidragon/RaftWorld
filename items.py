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
inv.Resource("Wood", 0)


#Fishing
imp.displayedTasks.append(task.Task(
name="Fishing",
cost={},
neededItems=[inv.lookup("Fishing Rod")],
time=7,
reward= {0.83: ( {inv.lookup("Fish"): 0}, "You could not catch a fish!"),
        0.96: ( {inv.lookup("Fish"): 1}, "You caught a sardine"),
        0.99: ( {inv.lookup("Fish"): 2}, "You caught a salmon"),
        1.0: ( {inv.lookup("Fish"): 5}, "You caught a tuna")},
cutChance = 0.075
))  

#Gather Seaweed
task.Task(name = "Gather Seaweed",
    cost = {},
    neededItems=[],
    time = 2,
    reward = {0.4: ({inv.lookup("Seaweed"): 0}, "You failed to gather seaweed"),
        0.7: ({inv.lookup("Seaweed"): 1}, "You found one piece of seaweed"),
        0.95: ({inv.lookup("Seaweed"): 3}, "You found a large blob of seaweed"),
        1: ({inv.lookup("Seaweed"): 6}, "You found piles of seaweed") },
    cutChance = 0.05
        )

def cleanBoatReward():
    pl.boat.all[0].decay -= 6

task.Task(name = "Clean Boat",
    cost = {},
        neededItems=[],
        time = 5,
        reward = cleanBoatReward
        cutChance = 0.025)

#Crafts Here!
(
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

woodPopUp = ev.Popup('A log floats near the raft...', 
optionTasks=[woodAcceptTask, declineTask])

def woodWeight():
    if not imp.boatUnlock:
        return 1_000_000_000_000

    return 2


ev.Event("Wood Floats By", minCooldown=100, screenPopup=woodPopUp, weightFunc = woodWeight)

#String Floats By
stringAcceptTask = task.Task("Swim towards it", {}, [], 1, { 
    0.3: ({inv.lookup("Fishing Reel"): 0}, "The fishing reel sunk too far"),
    1: ({inv.lookup("Fishing Reel"): 1}, "You managed to salvage one fishing reel")})

stringPopUp = ev.Popup('A fishing reel appears in the water...',
optionTasks=[stringAcceptTask, declineTask])

def reelWeight():
    return 2

ev.Event("String Floats By", minCooldown=100, screenPopup=stringPopUp, weightFunc = reelWeight)

#Boat Decay Initiation
def startBoatDecay():
    imp.boatDecay = True
    imp.outputMessage.append("Your boat starts to decay, you must manage this by cleaning and reinforcing the boat.", color = "#50C878")
    imp.displayedTasks.append(task.lookup("Clean Boat"))


boatDecayPopup = ev.Popup('Your boat starts to decay, you must manage this by cleaning and reinforcing the boat.', [], duration = 15)

def decayWeight():
    if imp.boatDecay:
        return 0

    return 10

ev.Event("Boat Starts Decay", minCooldown=140, screenPopup=boatDecayPopup, weightFunc = decayWeight, automaticFunc=startBoatDecay)




