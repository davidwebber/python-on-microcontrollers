import board
import digitalio
import time

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

delay = 0.5
i = 0
while True:
    print(f"Hello World! {i}")
    led.value = True
    time.sleep(delay)
    led.value = False
    time.sleep(delay)
    i += 1
