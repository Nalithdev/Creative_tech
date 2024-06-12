from machine import Pin, Timer, PWM
from servo import Servo
import time
import network
import urequests
import ujson

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

ssid = 'Nalith'
password = 'Drakspears'
wlan.connect(ssid, password)
url = "http://172.20.48.1:3000/pos"

while not wlan.isconnected():
    print('noco')
    time.sleep(1)

trig = Pin(16, Pin.OUT)
echo = Pin(17, Pin.IN, Pin.PULL_DOWN)
motor = Servo(15)
led = Pin(18, Pin.OUT)
timer1 = Timer()


def get_object():
    trig.value(0)
    time.sleep(0.1)
    trig.value(1)
    trig.value(0)
    while echo.value() == 0:
        pulse_start = time.ticks_us()
    while echo.value() == 1:
        pulse_end = time.ticks_us()
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17165 / 1000000
    distance = round(distance, 0)
    print('Distance:', "{:.0f}".format(distance), 'cm')
    if distance < 300:
        led.on()
        print("led on")
    else:
        led.off()
        print("led off")
    try:
        print("POST")

        dataP = {"position": distance}
        print(dataP)
        print(url)
        response = urequests.post(url, headers={'content-type': 'application/json'}, data=ujson.dumps(dataP))
        print("response:", response.text)
        print(response.json())
        print("bonjou")
        response.close()
        time.sleep(1)
    except Exception as e:
        print(e)


motor.move(180)
get_object()
time.sleep(0.8)
motor.move(0)
get_object()


def Motor():
    global motor
    motor.move(180)
    get_object()
    time.sleep(0.8)
    motor.move(0)
    get_object()


timer1.init(period=1600, mode=Timer.PERIODIC, callback=lambda t: Motor())  # Call buttonTimer every 100ms






