from pynput import mouse, keyboard
import pyautogui # this library has better mouse moving function

class ADo:
    def __init__(self, replayHotkey):
        self.events = []
        self.enableCaptureEvents = False
        self.stopHotkey = keyboard.Key.esc
        self.replayHotkey = keyboard.KeyCode.from_char(replayHotkey)

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

    def waitForInput(self):
        print('Waiting for hotkey input...')
        print('Press ` to replay. Press ESC to terminate.')
        with keyboard.Listener(
            on_press = self.callBackHotKeyPress
        ) as KL:
            KL.join()

    def callBackOnClick(self, x, y, button, pressed):
        if self.enableCaptureEvents:
            if pressed:
                print('Capture click {} event at {}'.format(button,(x,y)))
                self.events.append((x,y,button))
        else:
            return False

    def callBackOnPress(self, key):
        if self.enableCaptureEvents:        
            if key == self.stopHotkey:
                print('Stop capturing event!!!')
                self.enableCaptureEvents = False
                mouse.Controller().click(mouse.Button.left)
                return False
            else:
                print('Capture key press {}'.format(key))
                self.events.append(key)        

    def callBackHotKeyPress(self, key):
        if key == self.replayHotkey:
            print('Replay events!!!')
            self.replayEvents()
        if key == self.stopHotkey:
            print('Stop program!!!')
            return False

    def replayEvents(self):   
        mouseCtrl = mouse.Controller()
        keyboardCtrl = keyboard.Controller()
        for event in self.events:
            if type(event) is tuple:
                previousPosition = pyautogui.position()
                pyautogui.move(event[0] - previousPosition[0], event[1] - previousPosition[1])
                mouseCtrl.click(event[2])
            else:
                keyboardCtrl.press(event)
                keyboardCtrl.release(event)
                
"""
"" App Start
"""
if __name__ == "__main__":
    replayHotkey = '`'
    app = ADo(replayHotkey)
    app.captureEvents()
    app.waitForInput()