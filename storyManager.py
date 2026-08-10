import imports as imp
import inventoryLogic as inv
import taskLogic as task
import playerLogic as pl
import eventsLogic as ev

imp.outputMessage.append("Input Story Start")

boat = pl.Boat(durability=100, size=(6, 6))
player = pl.Player(name="Player", hunger=100)
gameTime = pl.gameTime()


imp.displayedResources.append(inv.Item("Fishing Rod", 1, breakable=True, breakChance=0.03))

imp.outputMessage.append("You have a fishing rod and a small boat. You need to catch some fish to survive. You also need to expand your boat to carry more resources.")

inv.Resource("Fish", 0, food = True, hungerScore=100)
inv.Resource("Seaweed", 0, food = True, hungerScore = 8)
imp.displayedResources.append(inv.Resource("Wood", 0))

inv.inventoryUpdate()



fish = task.Task(
    name="Fishing",
    cost={},
    neededItems=[inv.lookup("Fishing Rod")],
    time=6,
    reward= {0.8: ( {}, "You could not catch a fish!"),
            0.95: ( {inv.lookup("Fish"): 1}, "You caught a sardine"),
            0.99: ( {inv.lookup("Fish"): 2}, "You caught a salmon"),
            1.0: ( {inv.lookup("Fish"): 5}, "You caught a tuna")}
)

task.taskButtonUpdate()

def showSomething(div_id):
    boat_column = imp.document.querySelector(div_id)
    boat_column.style.display = "block"

async def hungerLoop():
    while True:
        player.hungerFrame()
        await imp.asyncio.sleep(1)

async def timeLoop():
    while True:
        gameTime.advance(3)

        pl.displayTime(gameTime)
        await imp.asyncio.sleep(0.5)

async def eventLoop():
    while True:
        ev.eventUpdate(gameTime.days)

        await imp.asyncio.sleep(1)


imp.asyncio.create_task(hungerLoop())
imp.asyncio.create_task(timeLoop())
imp.asyncio.create_task(eventLoop())
