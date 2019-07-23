import pyautogui # this library has better mouse moving function
from pynput import mouse, keyboard
from source.Event import Event
from time import sleep, clock

class ADo:
    def __init__(self):
        self.totalModes = 3
        self.replayMethods = [
            self.restartEventList,
            self.replayEventsAllAtOnce,
            self.replayEventsOneByOne,
            self.replayEventsWithDelay
        ]
        self.events = []
        self.enableCaptureEvents = False
        self.startHotkey = keyboard.Key.enter
        self.stopHotkey = keyboard.Key.esc
        self.replayModes = self.initReplayModes()
        self.mouseCtrl = mouse.Controller()
        self.keyboardCtrl = keyboard.Controller()
        self.startTime = 0

    def initReplayModes(self):
        replayModes = {}
        for idx, method in zip(
            range(0,self.totalModes + 1), 
            self.replayMethods
        ):
            key = keyboard.KeyCode()
            key.char = str(idx)
            replayModes[key] = method
        return replayModes

    def setStartTime(self):
        self.startTime = clock()         

    def getDelay(self):
        delay = round(clock() - self.startTime,2)
        self.startTime = clock()
        return delay

    def run(self):
        self.waitForCaptureCommand()
        self.waitForReplayCommand()    

    def captureEvents(self):
        self.enableCaptureEvents = True
        print('Start capturing events: ')
        with mouse.Listener(
            on_click = self.callBackOnClick
        ) as ML, keyboard.Listener(
            on_press = self.callBackOnPress
        ) as KL:
            KL.join()
            ML.join()
        return self.events

    def replayEvents(self, key):
        self.replayModes[key]()

    def replayOneEvent(self, event):
        if event.eventType == 'mouse':
            print('Replay click event {} at ({},{})'.format(event.button, event.x, event.y))
            previousPosition = pyautogui.position()
            pyautogui.move(event.x - previousPosition[0], event.y - previousPosition[1])
            self.mouseCtrl.click(event.button)
        else:
            print('Replay keyboard event {}'.format(event.button))
            self.keyboardCtrl.press(event.button)
            self.keyboardCtrl.release(event.button)

    def replayEventsAllAtOnce(self):
        for event in self.events:
            self.replayOneEvent(event)

    def replayEventsOneByOne(self):
        remainingReplayableEvents = sum([1 for event in self.events if event.isReplayed == False])
        if remainingReplayableEvents == 0:
            self.restartEventList()
        for event in self.events:
            if event.isReplayed == False:
                self.replayOneEvent(event)
                event.isReplayed = True
                break

    def replayEventsWithDelay(self):
        for event in self.events:
            print('Delay - {}'.format(event.delay))
            sleep(event.delay)
            self.replayOneEvent(event)

    def restartEventList(self):
        print('Restart event list !')
        for event in self.events:
            event.isReplayed = False

    def waitForCaptureCommand(self):
        print('Press Enter to start capturing events...')
        with keyboard.Listener(
            on_press = self.callBackStartCapture
        ) as KL:
            KL.join()

    def waitForReplayCommand(self):
        print('Waiting for hotkey input...')
        print('Press 1->{} to replay events. Press ESC to terminate.'.format(self.totalModes))
        with keyboard.Listener(
            on_press = self.callBackHotKeyPress
        ) as KL:
            KL.join()
    
    def callBackStartCapture(self, key):
        if key == self.startHotkey:
            self.captureEvents()
            return False

    def callBackOnClick(self, x, y, button, pressed):
        if (self.startTime == 0):
            self.setStartTime()
        if self.enableCaptureEvents:
            if pressed:
                print('Capture click {} event at {}'.format(button,(x,y)))
                self.events.append(Event('mouse',button,x,y, delay = self.getDelay()))
        else:
            return False

    def callBackOnPress(self, key):
        if self.startTime == 0:
            self.setStartTime()
        if self.enableCaptureEvents:        
            if key == self.stopHotkey:
                print('Stop capturing events!!!')
                self.enableCaptureEvents = False
                mouse.Controller().click(mouse.Button.left)
                return False
            else:
                print('Capture key press {}'.format(key))
                self.events.append(Event('keyboard',button = key,delay = self.getDelay()))        

    def callBackHotKeyPress(self, key):
        if key in self.replayModes:
            self.replayEvents(key)
        if key == self.stopHotkey:
            print('Stop program!!!')
            return False