import imports as imp
import inventoryLogic as inv
import taskLogic as task
import playerLogic as pl
import eventsLogic as ev
import items

boat = pl.Boat(durability=100, size=(6, 6))
player = pl.Player(name="Player", hunger=100)
gameTime = pl.gameTime()

pl.displayBoatSize(boat)

imp.outputMessage.append("You are stranded in the middle of a freshwater ocean with only a fishing rod and wooden raft to your name. You need to battle starvation by fishing and getting food.", color = "#50C878")

inv.inventoryUpdate()

task.taskButtonUpdate()


async def hungerLoop():
    while True:
        if imp.gamePaused:
            await imp.pause_aware_sleep(0.2)
            continue
        player.hungerFrame()
        await imp.pause_aware_sleep(1)

async def timeLoop():
    while True:
        if imp.gamePaused:
            await imp.pause_aware_sleep(0.2)
            continue
        gameTime.advance(3)
        pl.displayTime(gameTime)

        await imp.pause_aware_sleep(0.5)

async def eventLoop():
    while True:
        if imp.gamePaused:
            await imp.pause_aware_sleep(0.2)
            continue
        ev.eventUpdate(gameTime.days)

        await imp.pause_aware_sleep(1)

async def decayLoop():
    while True:
        if imp.gamePaused:
            await imp.pause_aware_sleep(0.2)
            continue
        boat.decayFrame()

        await imp.pause_aware_sleep(1)

#Main game loop
imp.asyncio.create_task(hungerLoop())
imp.asyncio.create_task(timeLoop())
imp.asyncio.create_task(eventLoop())
imp.asyncio.create_task(decayLoop())