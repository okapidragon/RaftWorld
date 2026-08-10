import imports as imp
import inventoryLogic as inv
import taskLogic as task
import playerLogic as pl

imp.outputMessage.append("Input Story Start")

boat = pl.Boat(durability=100, size=(6, 6))
player = pl.Player(name="Player", hunger=100)
gameTime = pl.gameTime()

wood = inv.Resource("Wood", 20)
inv.Resource("Fish", 0)
inv.Item("Fishing Rod", 1, breakable=True, breakChance=0.1)

imp.outputMessage.append("You have a fishing rod and a small boat. You need to catch some fish to survive. You also need to expand your boat to carry more resources.")

fish = task.Task(
    name="Fishing",
    cost={},
    neededItems=[inv.lookup("Fishing Rod")],
    time=1,
    reward= {0.75: ( {}, "You could not catch a fish!"),
            0.9: ( {inv.lookup("Fish"): 1}, "You caught a sardine"),
            0.97: ( {inv.lookup("Fish"): 2}, "You caught a salmon"),
            1.0: ( {inv.lookup("Fish"): 5}, "You caught a tuna")
            }
)

async def hungerLoop():
    while True:
        player.hungerFrame()
        await imp.asyncio.sleep(1)

async def timeLoop():
    while True:
        gameTime.advance(3)

        timeText = f"{gameTime.hours:02d}:{gameTime.minutes:02d}"
        imp.outputMessage.append(f"Time: {timeText}")
        await imp.asyncio.sleep(0.5)

imp.asyncio.create_task(hungerLoop())
imp.asyncio.create_task(timeLoop())