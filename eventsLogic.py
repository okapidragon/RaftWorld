class Popup:
    def __init__(self, text, taskDicts):
        self.text = text #Text displayed at top of popup

        self.taskDicts = taskDicts #Dictionary of {Task: Dialogue on it}
        # (i.e. text = "string appears", taskDicts = {Paddle: Paddle Towards})

class Event:
    def __init__(self, name, difficulty, minCooldown, screenPopup):
        self.name = name
        self.difficulty = difficulty
        self.minCooldown = minCooldown
        self.screenPopup = screenPopup
    