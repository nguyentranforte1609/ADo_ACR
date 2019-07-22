# ADo_ACR
Just a simple application for auto capturing and then replaying keyboard, mouse events.

# Requirements:
- OS: Window 7/10 (I developed & tested on this environment only)
- Python libraries:
  - pynput
  - pyautogui

# How to use:
1. Run main.py on terminal
2. Press ENTER to start capturing events
3. Do your task (e.g click on/type something)
4. Press ESC to stop capturing events.
5. Press one of the following keys:
   - Press 1: Replay all events without delay
   - Press 2: Replay event one by one.
     - Press 0 to restart
6. Press ESC to terminal the program

# Future works:
1. New mode: Replay all event with delay. The delay is recorded during capturing phase.
2. Make executable file
3. Make UI