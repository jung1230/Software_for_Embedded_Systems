import socket
import network
import esp32
from machine import Timer, ADC, Pin

# Global variables
temp = "0"  # measure temperature sensor data
hall = "0"  # measure hall sensor data
red_led_state = "OFF" # string, check state of red led, ON or OFF


def web_page():
    """Function to build the HTML webpage which should be displayed
    in client (web browser on PC or phone) when the client sends a request
    the ESP32 server.
    
    The server should send necessary header information to the client
    (YOU HAVE TO FIND OUT WHAT HEADER YOUR SERVER NEEDS TO SEND)
    and then only send the HTML webpage to the client.
    
    Global variables:
    temp, hall, red_led_state
    """
    global temp
    global hall
    global red_led_state
    
    html_webpage = """<!DOCTYPE HTML><html>
    <head>
    <title>ESP32 Web Server</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.2/css/all.css" integrity="sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr" crossorigin="anonymous">
    <style>
    html {
     font-family: Arial;
     display: inline-block;
     margin: 0px auto;
     text-align: center;
    }
    h1 { font-size: 3.0rem; }
    p { font-size: 3.0rem; }
    .units { font-size: 1.5rem; }
    .sensor-labels{
      font-size: 1.5rem;
      vertical-align:middle;
      padding-bottom: 15px;
    }
    .button {
        display: inline-block; background-color: #e7bd3b; border: none; 
        border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none;
        font-size: 30px; margin: 2px; cursor: pointer;
    }
    .button2 {
        background-color: #4286f4;
    }
    </style>
    </head>
    <body>
    <h1>ESP32 WEB Server</h1>
    <p>
    <i class="fas fa-thermometer-half" style="color:#059e8a;"></i> 
    <span class="sensor-labels">Temperature</span> 
    <span>"""+str(temp)+"""</span>
    <sup class="units">&deg;F</sup>
    </p>
    <p>
    <i class="fas fa-bolt" style="color:#00add6;"></i>
    <span class="sensor-labels">Hall</span>
    <span>"""+str(hall)+"""</span>
    <sup class="units">V</sup>
    </p>
    <p>
    RED LED Current State: <strong>""" + red_led_state + """</strong>
    </p>
    <p>
    <a href="/?red_led=on"><button class="button">RED ON</button></a>
    </p>
    <p>
    <a href="/?red_led=off"><button class="button button2">RED OFF</button></a>
    </p>
    </body>
    </html>"""
    return html_webpage

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
        sta_if.connect("MSI_5954", "1230456789")
        while not sta_if.isconnected():
            pass
    print('Connected to', sta_if.config('essid'))
    print('IP Address:', sta_if.ifconfig()[0])
    print('')
before_connect()
do_connect()

# •  Measure the onboard temperature sensor data and hall sensor data. 
temp = esp32.raw_temperature()
hall = esp32.hall_sensor()

print("Temperature is ")
print(temp)
print("Hall is ")
print(hall)


# •  Measure the state of the red LED.
red_led_pin = Pin(13, Pin.OUT)
if red_led_pin.value():
    red_led_state = "ON"
else :
    red_led_state = "OFF"



# •  Use the function web_page (present in the provided file) to create simple HTML text 
# to build the webpage with the sensor data and the LED pin values. The HTML text has 
# already been provided in the espserver.py. You can use the 3 variables defined in the 
# file (temp, hall, red_led_state) to measure the sensor and pin values. 
html_text = web_page()

# •  Create a HTTP server using the socket API to listen for incoming requests from any 
# client (browser on your local PC or phone connected to same Wi-Fi network).  
def start_server():
    global red_led_state
    global temp
    global hall
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(5)
    
    # •  Use an infinite loop: Whenever your ESP server receives a client request (e.g., pressing 
    # any button on the webpage), it should use the function web_page to update the HTML 
    # text with the current sensor values and LED state, send necessary HTTP headers and 
    # finally send the updated HTML text as the response to the client. 
    while True:
        conn, addr = s.accept()
        print("Got a connection from %s" % str(addr))
        request = conn.recv(1024)
        print("Content = %s" % str(request))

        if b"red_led=on" in request:
            red_led_pin.on()
            red_led_state = "ON"
        elif b"red_led=off" in request:
            red_led_pin.off()
            red_led_state = "OFF"
        temp = esp32.raw_temperature()
        hall = esp32.hall_sensor()
        html_text = web_page()  
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(html_text)
        conn.close()

start_server()

