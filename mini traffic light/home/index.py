#-*-coding:utf-8-*-
import RPi.GPIO as GPIO
import time
import spidev
from flask import Flask, request
from flask import render_template

app = Flask(__name__)

#사용할 핀 번호 설정
led_R = 20
led_G = 21
SERVO_PIN = 18
TRIG = 23
ECHO = 24

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.output(TRIG, False)

delay=0.5
ldr_channel = 0

#서보모터 PWM설정
GPIO.setup(SERVO_PIN, GPIO.OUT)
servo = GPIO.PWM(SERVO_PIN, 50)
servo.start(0)

#RED LED PWM설정
GPIO.setup(led_R, GPIO.OUT)
r = GPIO.PWM(led_R, 80)
r.start(0)

#GREEN LED PWM설정
GPIO.setup(led_G, GPIO.OUT)
g = GPIO.PWM(led_G, 100)
g.start(0)

#spi설정
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 100000

#아날로그 -> 디지털
def readadc(adcnum):
	if adcnum > 7 or adcnum < 0:
		return -1
		
	r=spi.xfer2([1, (8+adcnum) << 4, 0])
	
	data = ((r[1] & 3) << 8)+r[2]
	return data

@app.route("/")
def home():
    return render_template("index.html")
    
@app.route("/go")
def go():
    while True:
        ldr_val=readadc(ldr_channel)
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)
        while GPIO.input(ECHO) == False:
            start = time.time()
        while GPIO.input(ECHO) == True:
            stop = time.time()

        check_time = stop - start
        distance = check_time * 34300 / 2
        time.sleep(delay)
        print("LDR Value : %d"%(ldr_val))
        print("Distance : %.lf cm"%(distance))
        if distance <=15:
            g.ChangeDutyCycle(100)
            r.ChangeDutyCycle(0)
            servo.ChangeDutyCycle(10)
            if ldr_val > 550:
                g.ChangeDutyCycle(10)
            else:
                g.ChangeDutyCycle(100)

        else:
            r.ChangeDutyCycle(100)
            g.ChangeDutyCycle(0)
            servo.ChangeDutyCycle(5)
            if ldr_val > 550:
                r.ChangeDutyCycle(10)
            else:
                r.ChangeDutyCycle(100)

@app.route("/emer")
def emer():
    while True:
        r.ChangeDutyCycle(100)
        g.ChangeDutyCycle(0)
        servo.ChangeDutyCycle(5)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
