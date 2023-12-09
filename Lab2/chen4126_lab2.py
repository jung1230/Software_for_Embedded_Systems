from machine import RTC
from machine import Timer
from machine import ADC
from machine import Pin
from machine import PWM

# The program should start by asking the user to input the current date and time as shown 
# in the following format. Use the user inputs to initialize the RTC (real time clock). Use 
# the current time in the EDT time zone for entering the time.
Year = int(input("Year? "))
Month = int(input("Month? "))
Day = int(input("Day? "))
Weekdayy = int(input("Weekday? "))
Hour = int(input("Hour? "))
Minute = int(input("Minute? "))
Second = int(input("Second? "))
Microsecond = int(input("Microsecond? "))

rtc = RTC()
rtc.datetime((Year, Month, Day, Weekdayy, Hour, Minute, Second, Microsecond))

    # Use the real-time clock (RTC) and a hardware timer to display the current date and time 
    # every 30 seconds. Do not use time.sleep(). Use the RTC and a timer interrupt/callback 
    # instead.
def display_time(datetime):
    print(str(datetime[0]) + '/' + str(datetime[1]) + '/' + str(datetime[2]) + ' ' + str(datetime[4]) + ':' + str(datetime[5]) + ':' + str(datetime[6]) )

timer1 = Timer(1)
# pass the function itself as the callback, without calling it
timer1.init(period=30000,mode=Timer.PERIODIC,callback=lambda t:display_time(rtc.datetime()))

    # Initialize another hardware timer and read the analog input (potentiometer/pot values) 
    # every 100ms using the timer interrupt/callback and ADC. IMPORTANT: Connect the 
    # potentiometer only to a pin associated with ADC1 and not ADC2. 
adc = ADC(Pin(34)) #ADC1_CH6 
timer2 = Timer(2)
timer2.init(period=100,mode=Timer.PERIODIC,callback= lambda t:adc.read())

    # Initialize and start a PWM signal on the external LED using a frequency of 10 Hz and 
    # a duty cycle of 512 (50%). The LED should start blinking at the defined frequency.
led = PWM(Pin(26),freq=10,duty=512)



    # Detect a switch press using an interrupt/callback. Implement switch debouncing using 
    # another timer-based interrupt/callback. 
    # o  Alternate switch presses should direct control towards either the frequency or 
    # the duty cycle of the LED. 
    # o  The LED’s PWM signal frequency and duty cycle should be controlled by the 
    # pot readings. 
    # o  When you press the switch for the first time, the pot should control the LED’s 
    # PWM frequency. Now, if you rotate the pot, your LED should blink faster or 
    # slower,  as  the  frequency  of  PWM  changes.  No  change  should  occur  in  the 
    # LED’s intensity.
    # o  When you press the switch for the second time, the pot should control the LED’s 
    # PWM duty cycle. Now, if you rotate the pot, your LED’s intensity should be 
    # higher or lower, as the duty cycle of PWM changes. No change in the LED’s 
    # blinking frequency.
    # o  The third switch press should revert the control back to the frequency, the fourth 
    # press  should give  control  to the duty  cycle  and the  process  should continue 
    # forever. 
global button_pressed
button_pressed = 0

def press(pin):
    global button_pressed
    button_pressed = button_pressed + 1
    

button = Pin(38, Pin.IN, Pin.PULL_UP)
button.irq(trigger = Pin.IRQ_FALLING, handler = press)

while True:
    if(button_pressed != 0):
        if button_pressed % 2 == 1:
            temp = int((adc.read())/300 + 1)
            led.freq(temp)  # Set the frequency
        elif button_pressed % 2 == 0:
            temp = int((adc.read()/10) + 1)
            led.duty(temp)  # Set the duty cycle

 
    
