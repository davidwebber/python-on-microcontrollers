# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
import random
import time
import board
import digitalio
import adafruit_dotstar as dotstar

nLED = 72
# Using a DotStar Digital LED Strip with nLED LEDs connected to digital pins
dots = dotstar.DotStar(board.GP0, board.GP1, nLED, brightness=0.1, auto_write=False)

# Physical GPIO
# Pin  1 GP0 Yellow
# Pin  2 GP1 Green
# Pin 38 Ground
# Pin 40 Red VBUS
# Pin 21 GP16 push-button
# Pin 23 Ground

# Button setup.  Button is True if unpressed. 
button = digitalio.DigitalInOut(board.GP16)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP   # Uses internal pull-up resistor

# HELPERS
# a random color 0 -> 192
def random_color():
    return random.randrange(0, 7) * 32

def wait_for_button():
    while True:
        current_state = button.value
        if last_state and not current_state:
            break
        last_state = current_state
        time.sleep(0.1)

def lightsaber():
    global dots
    idle_color = (32,32,0)
    blade_color = (255,255,0)
    for i in range(nLED):
        dots[i] = (0,0,0)
    dots[0] = idle_color
    dots.show()
    wait_for_button()
    # ignite
    for i in range(nLED):
        dots[i] = blade_color
        #time.sleep(0.1)
        dots.show()
    wait_for_button()
    # retract
    for i in range(nLED,0,-1):
        dots[i] = (0,0,0)
        dots.show()
    
def larson_scanner():
    last_state = True
    pattern = [(100,0,0),(200,0,0),(255,0,0),(255,0,0),(200,0,0),(100,0,0)]
    _start = 0
    _end = nLED - len(pattern)
    direction = 1
    while True:
        for offset in range(_start, _end, _direction):
            for i in range(nLED):
                if i < offset or i >= offset+len(pattern):
                    dots[i] = (0,0,0)
                elif offset <= i and i < offset + len(pattern):
                    dots[i] = pattern[i-offset]
                current_state = button.value
                if not current_state and last_state:
                    return
                last_state = current_state
            dots.show()
        _start, _end, direction = _end, _start, -1*direction
    
def matrix():
    pass

def xmas():
    pass
            
# MAIN LOOP
while True:
    # Fill each dot with a random color
    #print("Filling Dots")
    for dot in range(nLED):
        #dots[dot] = (random_color(), random_color(), random_color())
        #dots[dot] = (0, random_color(), 0)
        dots[dot] = (random_color(), 0, 0)

    dots.show()
    wait_for_button()
    time.sleep(0.20)

    lightsaber()

    wait_for_button()

    larson_scanner()

    matrix()

    xmas()
    