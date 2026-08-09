import imports as imp
import inventoryLogic as inv
import taskLogic as task
from pyscript import document

print("Story starts")

wood = inv.Resource("Wood", 0)
document.querySelector("#wood-count").textContent = str(wood.quantity)


