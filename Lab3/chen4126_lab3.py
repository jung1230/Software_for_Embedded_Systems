import network
import ntptime
import time
from machine import RTC
from machine import Timer
from machine import TouchPad, Pin
import machine
import esp32
import neopixel
from machine import deepsleep

# ------------------------------------------ 2.2.4. Red LED, Deep Sleep, and Different Wake Up Sources ------------------------------------------
# The red LED should be ON whenever the ESP32 is awake and OFF when it is in sleep mode
red_led = machine.Pin(13, machine.Pin.OUT)
red_led.value(1)
# Configure the switch as an external wake-up source. Pressing the switch within the 1-minute sleep duration should wake up the board and print out it’s an EXT0 wake-up.
switch = machine.Pin(25, machine.Pin.IN)
#level parameter can be: esp32.WAKEUP_ANY_HIGH or esp32.WAKEUP_ALL_LOW
esp32.wake_on_ext0(switch, esp32.WAKEUP_ANY_HIGH)

# callback function for timer3
def Csleep(timer):
    print("I am going to sleep for 1 minute.\n")
    machine.deepsleep(60000)


# Use a third hardware timer to put the ESP32 into deep sleep every 30 seconds for a duration of 1 minute.
timer3 = Timer(3)
# pass the function itself as the callback, without calling it
timer3.init(period=30000,mode=Timer.ONE_SHOT, callback=Csleep)

# Check if the board woke up from deep sleep
wake_reason = machine.wake_reason()
if wake_reason != machine.PWRON_RESET:
    if wake_reason == 4:  # Constant 4 indicates wake from external source
        print("\nWoke up due to timer wakeup.\n")    
    else:
        print("\nWoke up due to EXT0 wakeup.\n")



# ------------------------------------------ 2.2.1. Connect to the Internet over WiFi ------------------------------------------
def before_connect():
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)

    # Seems more reliable to start with a fresh connect()
    if sta_if.isconnected():
        sta_if.disconnect()

def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.scan()  
    if not sta_if.isconnected():
        sta_if.connect("Campus Edge", "8884pavlov")
        while not sta_if.isconnected():
            pass
    print('Connected to', sta_if.config('essid'))
    print('IP Address:', sta_if.ifconfig()[0])
    print('')

before_connect()
do_connect()



# ------------------------------------------ 2.2.2. Display Current Date and Time using Network Time Protocol (NTP) ------------------------------------------
# Get the current time from the Internet using NTP.
ntptime.settime()

# Use it to set the RTC. Then, manually adjust the RTC to convert UTC to the current local time zone in West Lafayette.
rtc = RTC()
UTC = 4 * 60 * 60
tm = time.localtime(time.time() - UTC)
rtc.datetime((tm[0], tm[1], tm[2], 0,tm[3], tm[4], tm[5], 0))

# Similar to lab 2, initialize a hardware timer and display the current date & time every 15 seconds.
def display_time(datetime):
    print("Date: {:02d}/{:02d}/{:04d}\nTime: {:02d}:{:02d}:{:02d} HRS\n".format(datetime[1], datetime[2], datetime[0], datetime[4], datetime[5], datetime[6]))
timer1 = Timer(1)
# pass the function itself as the callback, without calling it
timer1.init(period=15000,mode=Timer.PERIODIC,callback=lambda t:display_time(rtc.datetime()))



# ------------------------------------------ 2.2.3. NeoPixel Control by Touch Input ------------------------------------------
# Initialize the Touchpad-enabled pin connected to the jumper wire and calibrate it by observing how the touchpad pin values change when you physically touch the jumper wire.
t = TouchPad(Pin(14))
t.config(500)               # configure the threshold at which the pin is considered touched

# callback function for timer2
def touch(timer):
    touch_value = t.read() 
    if touch_value < 500: 
        # Wire touched
        np[0] = (0, 255, 0)  # Set color to green
    else:
        # Wire not touched
        np[0] = (0, 0, 0)    # Turn off the NeoPixel
    
    np.write()
# initialize the neopixel
I2C = machine.Pin(2, machine.Pin.OUT) # Pin 2 is the I2C pin responsible for providing power to the neopixel
I2C.value(1) # set pin high
np = neopixel.NeoPixel(machine.Pin(0), 1) # pin 0, 1 pixel only

# Initialize a second hardware timer and read the touch pin values every 50 milliseconds using a Timer interrupt/callback and implement the following pattern. Use calibrated values to detect whether the wire is touched or not
timer2 = Timer(2)
# pass the function itself as the callback, without calling it
timer2.init(period=50,mode=Timer.PERIODIC, callback=touch)



