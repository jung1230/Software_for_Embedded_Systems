from machine import Pin
from time import sleep

# Onboard RED LED is connected to IO_X
# Find out X from schematics and datasheet
# Create output pin on GPIO_X
# X = 13
led_board = Pin(13, Pin.OUT)

for i in range(10):
    # change pin value
    led_board.value(not led_board.value())
    sleep(0.5)

print("Led blinked 5 times")