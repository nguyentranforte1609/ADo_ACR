class Event():
    def __init__(self, eventType, button=None, x=None, y=None, delay=0):
        self.eventType = eventType
        self.button = button
        self.x = x
        self.y = y
        self.isReplayed = False
        self.delay = delay