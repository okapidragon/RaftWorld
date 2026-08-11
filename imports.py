import random
import asyncio
import threading
import time
from pyscript import document  # pyright: ignore[reportMissingImports]

def displayOutput():
    output_column = document.querySelector("#output-col")

    output_column.innerHTML = "<h3 style=\"text-align: center;\">Output</h3>"

    for message in reversed(outputMessage.messages[-15:]):
        message_line = document.createElement("p")
        message_line.style.textAlign = "center"
        message_line.textContent = message
        output_column.appendChild(message_line)

class OutputMessage:
    def __init__(self):
        self.messages = []

    def append(self, message):
        self.messages.append(message)
        displayOutput()

def showSomething(div_id):
    boat_column = document.querySelector(div_id)
    boat_column.style.display = "block"

outputMessage = OutputMessage()

currentEvent = None

#Progression Variables
seaweedUnlock = False
boatUnlock = False

displayedResources = []
displayedTasks = []


