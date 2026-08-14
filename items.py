import imports as imp
import inventoryLogic as inv
import taskLogic as task
import eventsLogic as ev
import playerLogic as pl


#Items
imp.displayedResources.append(inv.Item("Fishing Rod", 1, breakable=True, breakChance=0.1))
inv.Item("Paddle", 0, breakable=True, breakChance=0.01)
inv.Item("Hammer", 0, breakable = True, breakChance = 0.04)
inv.Item("Spear", 0, breakable = True, breakChance = 0.05)
inv.Item("Anchor", 0)

#Relics
inv.Item("Merchant's Coin", 0, relic = True, color = "Gold")
inv.Item("Captain's Hat", 0, relic = True, color = "Brown") 
inv.Item("Shark's Head", 0, relic = True, color = "Blue")
inv.Item("Dynamite Rod", 0, relic = True, color = "Goldenrod")
inv.Item("Glowing Bass", 0, relic = True, color = "Purple")

#Resources
inv.Resource("Fish", 0, food = True, hungerScore=100)
inv.Resource("Seaweed", 0, food = True, hungerScore = 8, eatQuantity = 5)
inv.Resource("Fishing Reel", 0)
inv.Resource("Wood", 0)
inv.Resource("Gold", 0)
inv.Resource("Metal", 0)
inv.Resource("Explosive", 0)



#Fishing
imp.displayedTasks.append(task.Task(
name="Fishing",
cost={},
neededItems=[inv.lookup("Fishing Rod")],
time=7,
reward= {0.75: ( {inv.lookup("Fish"): 0}, "You could not catch a fish!"),
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
task.Task(name = "Craft Spear",
    cost = {inv.lookup("Wood"): 10, inv.lookup("Metal"): 4},
    neededItems=[],
    time = 3,
    reward = {1: ({inv.lookup("Spear"): 1}, "Succesful spear craft!")}, craft=True
)
task.Task(name = "Craft Anchor",
    cost = {inv.lookup("Metal"): 15},
    neededItems=[],
    time = 3,
    reward = {1: ({inv.lookup("Anchor"): 1}, "Succesful anchor craft!")}, craft=True
)

def relicCraft():
    imp.outputMessage.append("Succesfully obtained Dynamite Rod relic!")
    inv.lookup("Dynamite Rod").add(1)
    imp.displayedRelics.append(inv.lookup("Dynamite Rod"))
    inv.relicUpdate()

task.Task(name = "Craft Dynamite Rod",
    cost = {inv.lookup("Explosive"): 3, inv.lookup("Metal"): 10, inv.lookup("Fishing Reel"): 1},
    neededItems=[],
    time = 3,
    reward = relicCraft, craft=True
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

schoolOfFishPopup = ev.Popup("A school of fish swims below your boat... (Fishing Odds Bettered)", [], duration = 25)

def fishWeight():
    return 0.005 * ev.lookup("School of Fish").cooldown

def newFishReward():
    prob = imp.random.random()

    bassRelic = inv.lookup("Glowing Bass")

    fish = inv.lookup("Fish")

    if prob < 0.2:
        if bassRelic in imp.displayedRelics:
            imp.outputMessage.append("You could not catch a fish")
            return

        imp.outputMessage.append("Caught Glowing bass relic!")
        bassRelic.add(1)
        imp.displayedRelics.append(bassRelic)
        inv.relicUpdate()

    elif prob < 0.6:
        imp.outputMessage.append("You caught a sardine")
        fish.add(1)


    elif prob < 0.9:
        imp.outputMessage.append("You caught a salmon")
        fish.add(2)

    else:
        imp.outputMessage.append("You caught a tuna")
        fish.add(5)


async def fishSchool():
    fishing = task.lookup("Fishing")

    ogReward = fishing.reward

    fishing.reward = newFishReward

    await imp.pause_aware_sleep(18)

    fishing.reward = ogReward


ev.Event("School of Fish", 180, schoolOfFishPopup, fishWeight, automaticFunc=fishSchool)

#Large Wave

dropAnchor = task.Task(name = "Drop Anchor", cost ={}, neededItems=[inv.lookup("Anchor")], time = 2, 
                       reward = {1: ({}, "You dropped your anchor and avoided catastrophe.")})

largeWavePopup = ev.Popup("A large wave hits your raft. Your raft speeds up decay significantly.", [dropAnchor], duration = 10)

def largeWaveWeight():
    if pl.Boat.all[0].decay > 5 and imp.boatDecay:
        return 0.4 + ev.lookup("Large Wave").cooldown * 0.004 - 2.5

    return 0


def largeWaveFunc():
    pl.Boat.all[0].decaySpeed += 1.25
    pl.setDecayBarProgress(pl.Boat.all[0].decay)
    imp.outputMessage.append("A large wave hits your raft. Your raft speeds up decays significantly.", color = "Red")


ev.Event("Large Wave", 250, largeWavePopup, largeWaveWeight, stopFunc=largeWaveFunc, timer = False)

#Shipwreck 1

async def shipwreckExploreFunc():
    imp.outputMessage.append("You swim down to the shipwreck. What comes next must be done quickly!", color = "Red")

    await ev.stopEvent(shipwreckEvent)

    await imp.pause_aware_sleep(1)

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
    return 0.5 + (shipwreckEvent.cooldown - shipwreckEvent.minCooldown) * 0.004

shipwreckEvent = ev.Event(name = "Shipwreck", minCooldown = 180, screenPopup=shipwreckPopup, weightFunc=shipwreckWeight, cooldown = 0)
# Shipwreck 2
goldSalvage = task.Task("Collect Treasure",
                        cost = {},
                        neededItems = [],
                        time = 2,
                        reward = {1: ({inv.lookup("Gold"): 50}, "You salvaged 50 gold from the chest.")},
                        swimTroubleChance=0.2)


shipwreckWoodSalvage = task.Task("Salvage Wood",
                        cost = {},
                        neededItems = [],
                        time = 2,
                        reward = {1: ({inv.lookup("Wood"): 15}, "You salvaged 15 wood from the chest.")},
                        swimTroubleChance=0.2)

def captainHatReward():
    imp.outputMessage.append("You see the dead captain and take his legendary hat! You obtained the Captain's Hat relic!", color = "Green")
    inv.lookup("Captain's Hat").add(1)
    imp.displayedRelics.append(inv.lookup("Captain's Hat"))
    inv.relicUpdate()


secretDoorShipwreck = task.Task("Open Door",
                        cost = {},
                        neededItems = [inv.lookup("Hammer")],
                        time = 2,
                        reward = captainHatReward,
                        swimTroubleChance=0.2)

shipwreckDecisionPopup = ev.Popup("You quickly swim down to the shipwreck. You see a treasure chest and a secret door.", optionTasks=[goldSalvage, shipwreckWoodSalvage, secretDoorShipwreck], duration = 7)



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

explosiveTrade = task.Task("Get 20 Gold",
                      cost = {inv.lookup("Explosive"): 1},
                      neededItems=[],
                      time = 0,
                      reward = {1: ({inv.lookup("Gold"): 20}, "Traded for 20 Gold")})

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

def merchantCoinReward():
    imp.outputMessage.append("Traded for the Merchant's Coin!", color = "Green")
    inv.lookup("Merchant's Coin").add(1)
    imp.displayedRelics.append(inv.lookup("Merchant's Coin"))
    inv.relicUpdate()

merchantsCoinTrade = task.Task("Merchant's Coin",
                      cost = {inv.lookup("Gold"): 250},
                      neededItems=[],
                      time = 0,
                      reward = merchantCoinReward)

merchantPopup = ev.Popup("A merchant boat appears beside you. They do not want to stay but may trade with you...",
                         optionTasks = [fishTrade, explosiveTrade, metalTrade, hammerTrade])

def merchantWeight():
    return 1.5 + (merchantEvent.cooldown - merchantEvent.minCooldown) * 0.004

def merchantEnd():
    imp.metalUnlock = True

merchantEvent = ev.Event("Merchant", minCooldown = 150, screenPopup=merchantPopup, weightFunc=merchantWeight, cooldown = 30, multipleTasks=True, stopFunc = merchantEnd, randomItems = 3)

#Shark Event

def sharkLoss():
    imp.outputMessage.append("Lost the battle and got bitten by shark.")
    pl.Player.all[0].health -= 50
    pl.setHealthBarProgress(pl.Player.all[0].health)

def spearFunc():
    success = imp.random.random()

    if success < 0.75:
        imp.outputMessage("Won the battle with the shark and gained 8 Fish.")
        inv.lookup("Fish").add(8)

        if inv.lookup("Shark's Head") not in imp.displayedRelics:
            imp.outputMessage("You managed to get the Shark's Head!")
            inv.lookup("Shark's Head").add(1)
            imp.displayedResources.append(inv.lookup("Shark's Head"))
            inv.relicUpdate()
        
    else:
        sharkLoss()


spearTheShark = task.Task(name = "Spear the Shark", cost = {}, neededItems = [inv.lookup("Spear")], time = 5, reward = spearFunc, swimTroubleChance = 0.1)

paddleAway = task.Task(name = "Paddle Away", cost = {}, neededItems = [inv.lookup("Paddle")], time = 5, reward = {})

sharkPopup = ev.Popup(text = "You notice a shark below you...", optionTasks = [spearTheShark, paddleAway], duration = 20)

def sharkWeight():
    return 0.65 + (sharkEvent.cooldown - sharkEvent.minCooldown) * 0.004

sharkEvent = ev.Event(name = "Shark", minCooldown = 250, screenPopup=sharkPopup, weightFunc=sharkWeight, cooldown = 0, stopFunc = sharkLoss)

#Raft Breaking
hammerIt = task.Task(name = "Fix With Hammer", cost = {}, neededItems=[inv.lookup("Hammer")], time = 2, reward = {})

def fall():
    wood = inv.lookup("Wood")

    ogWood = wood.quantity

    wood.quantity = wood.quantity // 2

    imp.outputMessage.append(f"You lost {ogWood - wood.quantity} wood.")


    

inventoryFallingPopup = ev.Popup(text = "Some of your raft breaks off, you can fix it but your items will fall...", optionTasks = [hammerIt], duration = 15)

def raftBreakWeight():
    return 0.65 + (inventoryFallingEvent.cooldown - inventoryFallingEvent.minCooldown) * 0.004 


inventoryFallingEvent = ev.Event(name = "Raft Break", minCooldown = 300, screenPopup=inventoryFallingPopup, weightFunc= raftBreakWeight,cooldown = 150, stopFunc = fall)

#Craft Event
def rewardCrate():
    metalAdd = imp.random.randint(1, 4)

    inv.lookup("Metal").add(metalAdd)

    imp.metalUnlock = True

    woodAdd = imp.random.randint(2, 9)

    inv.lookup("Wood").add(woodAdd)

    imp.outputMessage.append(f"The crate had {woodAdd} wood and {metalAdd} metal.")

openCrate = task.Task(name = "Hammer Open", cost = {}, neededItems=[inv.lookup("Hammer"), inv.lookup("Paddle")], time = 10, reward = rewardCrate)

cratePopup = ev.Popup(text = "A lone crate floats by near the raft.", optionTasks = [openCrate, declineTask], duration = 15)

def crateWeight():
    return 0.65 + (crateEvent.cooldown - crateEvent.minCooldown) * 0.003 

crateEvent = ev.Event(name = "Crate", minCooldown = 300, cooldown = 0, screenPopup = cratePopup, weightFunc=crateWeight)

#Naval Mine 1
async def navalMineExploreFunc():
    imp.outputMessage.append("You swim down to the naval mine and will need to make a split second decision!", color = "Red")

    await ev.stopEvent(navalMineEvent1)

    await imp.pause_aware_sleep(2)

    imp.asyncio.create_task(navalMineEvent2.execute())

navalMineExplore = task.Task(name = "Swim & Explore", cost = {}, neededItems=[], time = 4, reward = navalMineExploreFunc, swimTroubleChance = 0.25)

steerAround = task.Task("Steer Around", {}, [], 0, {})

navalMinePopup = ev.Popup(text = "You spot a Naval mine (land mine in water) far down in the ocean", optionTasks= [navalMineExplore, steerAround], duration = 20)

def navalMineWeight():
    return 0.5 + (navalMineEvent1.cooldown - navalMineEvent1.minCooldown) * 0.004

navalMineEvent1 = ev.Event(name = "Naval Mine1", minCooldown = 300, cooldown = 150, screenPopup = navalMinePopup, weightFunc = navalMineWeight)

#Naval Mine 2
def salvageExplosivesFunc():
    prob = imp.random.random()

    if inv.lookup("Explosive") not in imp.displayedResources:
        imp.displayedResources.append(inv.lookup("Explosive"))

    if prob < 0.25:
        imp.outputMessage.append("The naval mine exploded on you and you took 40 damage.", color = "Red")

        pl.Player.all[0].health -= 40
        pl.setHealthBarProgress(pl.Player.all[0].health)
    else:
        explosiveCount = imp.random.randint(2, 4)

        imp.outputMessage.append(f"You succesfully salvaged {explosiveCount} naval mine explosives.")

        inv.lookup("Explosive").add(explosiveCount)



salvageExplosives = task.Task(
    name = "Collect Explosives",
    cost = {},
    neededItems = [],
    time = 1.5,
    reward = salvageExplosivesFunc,
    swimTroubleChance = 0.4
)

navalMinePopup2 = ev.Popup(text = "You swim down near the naval mine... (Explosives are RISKY)", optionTasks = [salvageExplosives, declineTask], duration = 7)

navalMineEvent2 = ev.Event(name = "Naval Mine2", minCooldown = 0, screenPopup = navalMinePopup2, weightFunc = nullWeight)

#Cartographer