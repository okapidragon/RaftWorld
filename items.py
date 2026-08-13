import imports as imp
import inventoryLogic as inv
import taskLogic as task
import eventsLogic as ev
import playerLogic as pl


#Items
imp.displayedResources.append(inv.Item("Fishing Rod", 1, breakable=True, breakChance=0.07))
inv.Item("Paddle", 0, breakable=True, breakChance=0.01)
inv.Item("Hammer", 0, breakable = True, breakChance = 0.04)

#Resources
inv.Resource("Fish", 0, food = True, hungerScore=100)
inv.Resource("Seaweed", 0, food = True, hungerScore = 8, eatQuantity = 5)
inv.Resource("Fishing Reel", 0)
inv.Resource("Wood", 0)
inv.Resource("Gold", 0)
inv.Resource("Metal", 0)



#Fishing
imp.displayedTasks.append(task.Task(
name="Fishing",
cost={},
neededItems=[inv.lookup("Fishing Rod")],
time=7,
reward= {0.80: ( {inv.lookup("Fish"): 0}, "You could not catch a fish!"),
        0.95: ( {inv.lookup("Fish"): 1}, "You caught a sardine"),
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
#Clean Boat!
def cleanBoatReward():
    pl.Boat.all[0].decaySpeed -= 0.4
    pl.setDecayBarProgress(pl.Boat.all[0].decay)
    imp.outputMessage.append("Succesfully cleaned boat to slow decay.")

task.Task(name = "Clean Boat",
    cost = {},
        neededItems=[],
        time = 5,
        reward = cleanBoatReward,
        cutChance = 0.025)

#Reinforce Boat!
def reinforceReward():
    boat = pl.Boat.all[0]
    boat.decay = 0
    boat.decaySpeed -= 1.5
    imp.outputMessage.append("Boat reinforcement complete. Reset boat decay and reduced decay speed.")

task.Task(name = "Reinforce Boat",
    cost = {inv.lookup("Wood"): 8, inv.lookup("Seaweed"): 14},
    neededItems = [],
    time = 10,
    reward=reinforceReward, 
    cutChance = 0.1)

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
def nullWeight():
    return 0

#Wood floating by event!
woodAcceptTask = task.Task("Paddle to it", {}, [inv.lookup("Paddle")], 1, {
    0.3: ({inv.lookup("Wood"): 0}, "The wood floated away"),
    1: ({inv.lookup("Wood"): 10}, "You managed to salvage ten wood")})

woodPopUp = ev.Popup('A log floats near the raft...', 
optionTasks=[woodAcceptTask, declineTask])

def woodWeight():
    if not imp.boatUnlock:
        return 1_000_000_000_000

    return 1.5


ev.Event("Wood Floats By", minCooldown=100, screenPopup=woodPopUp, weightFunc = woodWeight)

#String Floats By
stringAcceptTask = task.Task("Swim towards it", {}, [], 1, { 
    0.3: ({inv.lookup("Fishing Reel"): 0}, "The fishing reel sunk too far"),
    1: ({inv.lookup("Fishing Reel"): 1}, "You managed to salvage one fishing reel")})

stringPopUp = ev.Popup('A fishing reel appears in the water...',
optionTasks=[stringAcceptTask, declineTask])

def reelWeight():
    return 1.5

ev.Event("String Floats By", minCooldown=100, screenPopup=stringPopUp, weightFunc = reelWeight)

#Boat Decay Initiation
def startBoatDecay():
    if not imp.boatDecayShown:
        imp.displayedTasks.append(task.lookup("Clean Boat"))
        imp.displayedTasks.append(task.lookup("Reinforce Boat"))
        imp.showSomething("#decay-section")
        imp.boatDecayShown = True
    imp.boatDecay = True
    imp.outputMessage.append("Your boat starts to decay, you must manage this by cleaning and reinforcing the boat.", color = "#50C878")
    task.taskButtonUpdate()


boatDecayPopup = ev.Popup('Your boat starts to decay, you must manage this by cleaning and reinforcing the boat.', [], duration = 15)

def decayWeight():
    if imp.boatDecay or imp.eventNumber <= 4:
        return 0

    return 100_000

ev.Event("Boat Starts Decay", minCooldown=140, screenPopup=boatDecayPopup ,weightFunc = decayWeight, automaticFunc=startBoatDecay, timer=False)

#School of Fish

schoolOfFishPopup = ev.Popup("A school of fish swims below your boat... (Fishing Odds Bettered)", [], duration = 18)

def fishWeight():
    return 0.005 * ev.lookup("School of Fish").cooldown

async def fishSchool():
    fishing = task.lookup("Fishing")

    ogReward = fishing.reward

    fishing.reward = {0.1: ( {inv.lookup("Fish"): 0}, "You could not catch a fish!"),
        0.60: ( {inv.lookup("Fish"): 1}, "You caught a sardine"),
        0.90: ( {inv.lookup("Fish"): 2}, "You caught a salmon"),
        1.0: ( {inv.lookup("Fish"): 5}, "You caught a tuna")}

    await imp.pause_aware_sleep(18)

    fishing.reward = ogReward


ev.Event("School of Fish", 180, schoolOfFishPopup, fishWeight, automaticFunc=fishSchool)

#Large Wave

largeWavePopup = ev.Popup("A large wave hits your raft. Your raft speeds up decay significantly.", [], duration = 8)

def largeWaveWeight():
    if pl.Boat.all[0].decay > 5 and imp.boatDecay:
        return 0.4 + ev.lookup("Large Wave").cooldown * 0.01 - 2.5

    return 0


def largeWaveFunc():
    pl.Boat.all[0].decaySpeed += 1.25
    pl.setDecayBarProgress(pl.Boat.all[0].decay)
    imp.outputMessage.append("A large wave hits your raft. Your raft speeds up decays significantly.", color = "Red")


ev.Event("Large Wave", 250, largeWavePopup, largeWaveWeight, automaticFunc=largeWaveFunc, timer = False)

#Shipwreck 1

async def shipwreckExploreFunc():
    imp.outputMessage.append("You swim down to the shipwreck. What comes next must be done quickly!", color = "Red")

    await ev.stopEvent(shipwreckEvent)

    await imp.asyncio.sleep(1)

    imp.asyncio.create_task(shipwreckDecisionEvent.execute())

paddleAndSwimDown = task.Task(name = "Explore It",
                              cost = {},
                             neededItems=[inv.lookup("Paddle")],
                             time  = 2,
                             reward = shipwreckExploreFunc,
                             swimTroubleChance=0.4)

shipwreckPopup = ev.Popup("You see an old abondoned shipwreck off in the distance...", 
                          optionTasks=[paddleAndSwimDown, declineTask])

def shipwreckWeight():
    if not imp.merchantUnlock:
        return 0.4

    return 0.6

shipwreckEvent = ev.Event(name = "Shipwreck", minCooldown = 220, screenPopup=shipwreckPopup, weightFunc=shipwreckWeight)
# Shipwreck 2
goldSalvage = task.Task("Collect Treasure",
                        cost = {},
                        neededItems = [],
                        time = 2,
                        reward = {1: ({inv.lookup("Gold"): 100}, "You salvaged 100 gold from the chest.")},
                        swimTroubleChance=0.2)


shipwreckWoodSalvage = task.Task("Salvage Wood",
                        cost = {},
                        neededItems = [],
                        time = 2,
                        reward = {1: ({inv.lookup("Wood"): 18}, "You salvaged 18 wood from the chest.")},
                        swimTroubleChance=0.2)



shipwreckDecisionPopup = ev.Popup("You quickly swim down to the shipwreck. You see a treasure chest.", optionTasks=[goldSalvage, shipwreckWoodSalvage], duration = 7)



shipwreckDecisionEvent = ev.Event(name = "Shipwreck Decision", 
                                  minCooldown = 0,
                                  screenPopup=shipwreckDecisionPopup,
                                  weightFunc=nullWeight)

#Traveling Merchant

fishTrade = task.Task("Get 7 Gold",
                      cost = {inv.lookup("Fish"): 1},
                      neededItems=[],
                      time = 0,
                      reward = {1: ({inv.lookup("Gold"): 7}, "Traded for 7 Gold")})

metalTrade = task.Task("Get 1 Metal",
                      cost = {inv.lookup("Gold"): 15},
                      neededItems=[],
                      time = 0,
                      reward = {1: ({inv.lookup("Metal"): 1}, "Traded for 1 Metal")})

hammerTrade = task.Task("Get 1 Hammer",
                      cost = {inv.lookup("Gold"): 150},
                      neededItems=[],
                      time = 0,
                      reward = {1: ({inv.lookup("Hammer"): 1}, "Traded for 1 Hammer")})

merchantPopup = ev.Popup("A merchant boat appears beside you. They do not want to stay but may trade with you...",
                         optionTasks = [fishTrade, metalTrade, hammerTrade])

def merchantWeight():
    return 1

merchantEvent = ev.Event("Merchant", minCooldown = 150, screenPopup=merchantPopup, weightFunc=merchantWeight, cooldown = 0, multipleTasks=True)



