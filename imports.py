import random
import asyncio
import threading
import inspect
import time
from pyscript import document, when  # pyright: ignore[reportMissingImports]
gamePaused = False


def displayOutput():
    output_column = document.querySelector("#output-fade")

    output_column.innerHTML = "<h3 style=\"text-align: center;\">Output</h3>"

    for message in reversed(outputMessage.messages[-15:]):
        message_line = document.createElement("p")
        message_line.style.textAlign = "center"
        message_line.innerHTML = message
        output_column.appendChild(message_line)

async def pause_aware_sleep(seconds: float):
    chunk = 0.2
    remaining = float(seconds)
    while remaining > 0:
        if gamePaused:
            await asyncio.sleep(0.1)
            continue
        wait = chunk if remaining >= chunk else remaining
        await asyncio.sleep(wait)
        remaining -= wait


class OutputMessage:
    def __init__(self):
        self.messages = []

    def append(self, message, color = "black"):
        self.messages.append(f"<span style=\"color: {color};\">{message}</span>")
        displayOutput()

def showSomething(div_id):
    boat_column = document.querySelector(div_id)
    # Clear any inline display so CSS rules (e.g. flex) can take effect
    boat_column.style.display = ""

def hideSomething(div_id):
    boat_column = document.querySelector(div_id)
    boat_column.style.display = "none"

outputMessage = OutputMessage()

currentEvent = None

timeSinceEvent = 0

#Progression Variables
seaweedUnlock = False
boatUnlock = False
boatDecay = False
boatDecayShown = False
craftingShown = False
eventNumber = 0
merchantUnlock = False

metalUnlock = False

displayedResources = []
displayedTasks = []
displayedCrafts = []

countdown = 0

@when("click", "#pause-button")
def toggle_pause(event):
    global gamePaused

    gamePaused = not gamePaused

    btn = document.querySelector("#pause-button")

    if gamePaused:
        btn.textContent = "Resume"
        outputMessage.append("Game paused.")
    else:
        btn.textContent = "Pause"
        outputMessage.append("Game resumed.")

    buttons = document.querySelectorAll("button")

    for b in buttons:
        if b.id == "pause-button":
            continue
        b.disabled = gamePaused

def death(message):
    body = document.body
    body.innerHTML = ""
    body.style.margin = "0"
    body.style.height = "100vh"
    body.style.display = "grid"
    body.style.placeItems = "center"
    body.style.padding = "30px"
    message_shown = document.createElement("h1")
    message_shown.innerHTML = message
    body.appendChild(message_shown)

def health_death():
    
    death("You ran out of health. You fall unconscious and die, staying on your raft until the end of time.")

def boat_death():
    death("Your boat fully decays, and falls apart. You fall into the water, and urgently swim around, trying to find something to save you. Your struggle eventually stops, and you sink to the bottom of the ocean and drown.")
