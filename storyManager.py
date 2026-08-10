import imports as imp
import inventoryLogic as inv
import taskLogic as task
import playerLogic as pl

imp.outputMessage.append("Input Story Start")

boat = pl.Boat(durability=100, size=(6, 6))
player = pl.Player(name="Player", hunger=100)

wood = inv.Resource("Wood", 20)
inv.Resource("Fish", 0)
inv.Item("Fishing Rod", 1, breakable=True, breakChance=0.1)

imp.outputMessage.append("You have a fishing rod and a small boat. You need to catch some fish to survive. You also need to expand your boat to carry more resources.")

fish = task.Task(
    name="Fishing",
    cost={},
    neededItems=[inv.lookup("Fishing Rod")],
    time=1,
    reward={1: {inv.lookup("Fish"): 1}}
)

async def hungerLoop():
    while True:
        player.hungerFrame()
        #For testing purposes, print the player's hunger level to the console
        print(f"Hunger: {player.hunger}")
        await imp.asyncio.sleep(1)

imp.asyncio.run(hungerLoop())


