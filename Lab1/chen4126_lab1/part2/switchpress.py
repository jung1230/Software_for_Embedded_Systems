import neopixel
import machine
from time import sleep

def turn_green():
    np[0] = (0, 25, 0)
    np.write()

def turn_red():
    np[0] = (25, 0, 0)
    np.write()

# this part is for neoPixel, make it shine in red
tt = machine.Pin(2, machine.Pin.OUT) # Pin 2 is the I2C pin responsible for providing power to the neopixel
tt.value(1) # set pin high
np = neopixel.NeoPixel(machine.Pin(0), 1) # pin 0, 1 pixel only
np[0] = (25, 0, 0)
np.write()

button = machine.Pin(38, machine.Pin.IN)
press_count = 0

while press_count < 5:
    # button pressed
    if button.value() == 0 :  
        turn_green()
        # if users keep pressing the button
        while button.value() == 0: 
            pass
        turn_red()
        press_count += 1
        
np[0] = (0, 0, 0)
np.write()      
print("You have successfully implemented LAB1!")