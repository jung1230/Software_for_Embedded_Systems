import network
from machine import SoftI2C, Pin 
from imu import MPU6050
import time
import urequests
from machine import Timer
import neopixel


# ---------------------------- 3.1. Software Initialization ----------------------------
accel_offset = [0, 0, 0]

def mpu_setup():
    global accel_offset
    i2c = SoftI2C(scl=Pin(14), sda=Pin(22))
    imu = MPU6050(i2c)

    # Calibrate by taking the average of initial readings
    calibration_samples = 50

    for i in range(calibration_samples):
        accel_offset = [sum(x) for x in zip(accel_offset, imu.accel.xyz)]
        time.sleep(0.1) 

    accel_offset = [x / calibration_samples for x in accel_offset]

mpu_setup()

# ---------------------------- 4. Setup ThingSpeak and IFTTT  ----------------------------
def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)

    # Seems more reliable to start with a fresh connect()
    if sta_if.isconnected():
        sta_if.disconnect()
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
    
do_connect()


# ------------------ system has detected MOTION---------------------
def detect_motion():
    global accel_offset
    global gyro_offset 
    i2c = SoftI2C(scl=Pin(14), sda=Pin(22))
    imu = MPU6050(i2c)

    accel_data = [x - offset for x, offset in zip(imu.accel.xyz, accel_offset)]
    print("Calibrated Accelerometer:", accel_data)
    if accel_data[0] > 0.1 or accel_data[0] < -0.1 or accel_data[1] > 0.1 or accel_data[1] < -0.1 or accel_data[2] > 0.1 or accel_data[2] < -0.1:
        led_board.value(1)
        print("Threshold Exceeded\n\n\n\n\n\n\n")
        send_data = {'value1': str(accel_data[0]), 'value2': str(accel_data[1]), 'value3': str(accel_data[2])}
        req_headers = {'Content-Type': 'application/json'}
        req = urequests.post('https://maker.ifttt.com/trigger/MotionDetected/json/with/key/d7hFfw4pvMQKfmUWAAu9QHeZ0wFxOzG7B1vLfAfzpg6', json=send_data, headers=req_headers)
        req.close()




# ---------------------------- 4.2.  ThingSpeak Setup   ----------------------------
# alarm_status = 1 means activate, = 0 means deactivate
alarm_status = 0
neo = Pin(0, Pin.OUT) 
neo_power = Pin(2, Pin.OUT) 
neo_power.value(1)
np = neopixel.NeoPixel(neo, 1)

led_board = Pin(13, Pin.OUT)
led_board.value(0)
timer2 = None
def check_status():
    global timer_status
    global timer2
    if timer2 is not None:
            timer2.deinit()
            timer2 = None
    ts_get = urequests.get('https://api.thingspeak.com/channels/2367299/feeds.json?api_key=9B64MSE2V91OSTFU&results=2').json()
    ts_data = ts_get['feeds'][1]['field1']
    if ts_data == "1":
        np[0] = (0, 255, 0)
        np.write()
        timer2=Timer(2)
        timer2.init(period=1000,mode=Timer.PERIODIC,callback = lambda t:detect_motion())
    else:
        # Cancel existing timer
        if timer2 is not None:
            timer2.deinit()
            timer2 = None
        np[0] = (0, 0, 0)
        np.write()
        led_board.value(0)
        time.sleep(30) 


timer1=Timer(1)
timer1.init(period=30000,mode=Timer.PERIODIC,callback = lambda t:check_status())




