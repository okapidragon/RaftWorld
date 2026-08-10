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

def displayBoatSize(boat):
    size_display = imp.document.querySelector("#boat-size")
    size_display.textContent = f"Boat size: {boat.size[0]} x {boat.size[1]}"

displayBoatSize(boat)

def resizeBoat(event=None):
    width_input = imp.document.querySelector("#boat-width")
    height_input = imp.document.querySelector("#boat-height")

    width = int(width_input.value)
    height = int(height_input.value)
    new_size = (width, height)

    try:
        old_area = boat.size[0] * boat.size[1]
        new_area = width * height

        if new_area > old_area:
            wood_needed = new_area - old_area
            if inv.lookup("Wood").quantity >= wood_needed:
                inv.lookup("Wood").remove(wood_needed)
                boat.size = new_size
                imp.outputMessage.append(f"Boat size changed to {boat.size[0]} x {boat.size[1]}, You used {wood_needed} wood.")
                displayBoatSize(boat)
            else:
                imp.outputMessage.append(f"Not enough wood to resize the boat. You need {wood_needed - inv.lookup('Wood').quantity} more wood.")
        if new_area < old_area:
            if new_area < 5 * 5:
                imp.outputMessage.append("Boat size cannot be smaller than 5 x 5.")
                return
            else: 
                wood_receiving = old_area - new_area
                inv.lookup("Wood").add(wood_receiving)
                boat.size = new_size
                imp.outputMessage.append(f"Boat size changed to {boat.size[0]} x {boat.size[1]}. You received {wood_receiving} wood.")
                displayBoatSize(boat)
    except ValueError:
        imp.outputMessage.append("Invalid input for boat size. Please enter valid integers.")
resize_button = imp.document.querySelector("#resize-boat-button")
resize_button.onclick = resizeBoat