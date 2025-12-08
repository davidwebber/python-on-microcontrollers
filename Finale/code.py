# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
import random
import time
import board
import adafruit_dotstar as dotstar

# Using a DotStar Digital LED Strip with 30 LEDs connected to digital pins
dots = dotstar.DotStar(board.GP0, board.GP1, 72, brightness=0.1, auto_write=False)

# Pin  1 GP0 Yellow
# Pin  2 GP1 Green
# Pin 38 Ground
# Pin 40 Red VBUS

# HELPERS
# a random color 0 -> 192
def random_color():
    return random.randrange(0, 7) * 32

# MAIN LOOP
n_dots = len(dots)
while True:
    # Fill each dot with a random color
    #print("Filling Dots")
    for dot in range(n_dots):
        #dots[dot] = (random_color(), random_color(), random_color())
        #dots[dot] = (0, random_color(), 0)
        dots[dot] = (random_color(), 0, 0)

    dots.show()
    time.sleep(0.20)
