import imports as imp
import inventoryLogic as inv
import taskLogic as task
import boatLogic as bt
from pyscript import document  # pyright: ignore[reportMissingImports]

imp.outputMessage += "Input Story Start"



boat = bt.Boat(durability=100, size=(6, 6))

wood = inv.Resource("Wood", 20)
inv.Resource("Fish", 0)
inv.Item("Fishing Rod", 1, breakable=True, breakChance=0.1)

imp.outputMessage += "You have a fishing rod and a small boat. You need to catch some fish to survive. You also need to expand your boat to carry more resources."

fish = task.Task(
    name="Fishing",
    cost={},
    neededItems=[inv.lookup("Fishing Rod")],
    time=1,
    reward={1: {inv.lookup("Fish"): 1}}
)

for item in inv.Resource.all:
    item_id = item.name.lower().replace(" ", "-")
    resource_line = document.createElement("p")
    resource_line.id = f"{item_id}-count"
    resource_line.textContent = f"{item.name}: {item.quantity}"
    document.querySelector("#inventory-col").appendChild(resource_line)

