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

black = (0,0,0)
blue  = (0,0,255)
white = (255,255,255)
green = (0,255,0)
red   = (255,0,0)

# HELPERS
# a random color 0 -> 192
def random_color():
    return random.randrange(0, 7) * 32

def wait_for_button():
    last_state = True
    time.sleep(0.1)
    while True:
        current_state = button.value
        if last_state and not current_state:
            break
        last_state = current_state
        time.sleep(0.1)
    while not button.value:
        time.sleep(0.1)

def wait_for_button_release():
    last_state = False
    while True:
        current_state = button.value
        if not last_state and current_state:
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
    speed = 5
    for i in range(0, nLED, speed):
        for j in range(nLED):
            dots[j] = blade_color if j<i else black
        dots.show()
    wait_for_button()
    # retract
    for i in range(nLED-1,-1,-1*speed):
        for j in range(nLED):
            dots[j] = blade_color if j<i else black
        dots.show()
    dots[:] = [black] * nLED
    dots.show()
    
def larson_scanner():
    last_state = True
    pattern = [
        ( 50,0,0),
        (100,0,0),
	(200,0,0),
	(255,0,0),
	(255,0,0),
	(200,0,0),
	(100,0,0),
        ( 50,0,0)
        ]
    _start = 0
    _end = nLED - len(pattern)
    _speed = 3
    while True:
        for offset in range(_start, _end, _speed):
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
        _start, _end, _speed = _end, _start, -1*_speed
    
def matrix():
    global dots
    dots[0] = (0,100,0) 

def xmas():
    global dots
    blue_white = [blue]*3 + [black]*3 + [white]*3 + [black]*3
    red_green  = [red]*3  + [black]*3 + [green]*3 + [black]*3
    max_bright = 100
    min_bright = 0
    speed = -5
    pattern = red_green
    n_pattern = 0
    last_state = True
    while True:
        for b in range(max_bright, min_bright, speed):
            for i in range(nLED):
                color = pattern[i % len(pattern)]
                dots[i] = (color[0]*b/100, color[1]*b/100, color[2]*b/100)
            dots.show()
            current_state = button.value
            if not current_state and last_state:
                return
            last_state = current_state
        max_bright, min_bright, speed = min_bright, max_bright, -1*speed
        if b > 80:
            time.sleep(1)
        if b < 20:
            if n_pattern == 0:
                pattern = blue_white
                n_pattern = 1
            else:
                pattern = red_green
                n_pattern = 0
            
# MAIN LOOP
while True: 
    print("starting lightsaber")
    lightsaber()
    print("stopping lightsaber")
   
    dots[0]=(32,0,0)
    dots.show()
    print("waiting for button")
    wait_for_button()

    print("starting larson scanner")
    larson_scanner()
    dots[:] = [black]*nLED
    print("stopping larson scanner")
    """
    dots[0]=(0,32,0)
    dots.show()
    print("waiting for button")
    wait_for_button()

    print("starting matrix")
    matrix()
    print("stopping matrix")
    """
    dots[0]=(32,0,0)
    dots[1]=(0,32,0)
    dots.show()
    print("waiting for button")
    wait_for_button()

    print("starting xmas")
    xmas()
    print("stopping xmas")
    
