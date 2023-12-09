import network
from machine import Timer, ADC, Pin
import esp32
import urequests
import utime
import sys
# ------------------- 2.3.2.   ESP32 Program (espclient.py)   -------------------
# •  Connect to the Internet and print out the local IP address (same as Section 2.2).
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

# •  Initialize a hardware timer with a period of 30 seconds. When the timer fires, perform the following operations: 
# o  Measure the onboard temperature sensor data and hall sensor data. 
# o  Print both the measured data onto the terminal. 
# o  Send these data to ThingSpeak cloud server using a socket API and HTTP GET request. You need to use your specific Write API Key to upload data to your channel in your ThingSpeak account. 
# Function to send data to ThingSpeak
def send_to_thingspeak(api_key, field1, field2):
    url = "http://api.thingspeak.com/update?api_key={}&field1={}&field2={}".format(api_key, field1, field2)
    response = urequests.get(url)
    response.close()
    
def measure(timer1):
    temperature = str(esp32.raw_temperature())
    hall_sensor = str(esp32.hall_sensor())

    print("Temperature is " + temperature)
    print("Hall is " + hall_sensor)
    send_to_thingspeak('QSI5D0M8ZID1Z7ME', temperature, hall_sensor)  


timer1 = Timer(1)
timer1.init(period=30000,mode=Timer.PERIODIC, callback=measure)

# •  Run your program for 5 minutes. 
def stop_program(timer):
    global timer1
    global stop_timer
    # Stop timer after 5 minute
    timer1.deinit()
    stop_timer.deinit()
    print("end")

stop_timer = Timer(2)
stop_timer.init(period=300000, mode=Timer.ONE_SHOT, callback=stop_program)
