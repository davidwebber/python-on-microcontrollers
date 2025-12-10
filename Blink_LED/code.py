import board
import digitalio
import time

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

delay = 0.5
while True:
    print("Hello World!")
    led.value = True
    time.sleep(delay)
    led.value = False
    time.sleep(delay)
