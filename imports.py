import random
import threading
import time
from pyscript import document  # pyright: ignore[reportMissingImports]



class OutputMessage:
    def __init__(self):
        self.messages = []

    def append(self, message):
        self.messages.append(message)
        displayOutput()
outputMessage = OutputMessage()

def displayOutput():
    output_column = document.querySelector("#output-col")

    for message in outputMessage[-4:]:
        message_line = document.createElement("p")
        message_line.textContent = message
        output_column.appendChild(message_line)