import random
import threading
import time



class OutputMessage:
    def __init__(self):
        self.messages = []

    def append(self, message):
        self.messages.append(message)

outputMessage = OutputMessage()