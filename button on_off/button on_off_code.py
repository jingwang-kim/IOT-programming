import RPi.GPIO as GPIO
import time

button_pin = 15
led_pin = 4

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(button_pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(led_pin, GPIO.OUT)

p=GPIO.PWM(led_pin, 50)
p.start(0)

light_on = False

def button_callback(channel):
	global light_on
	if light_on == False:
                print("LED ON!")
		while True:
			dc=0
			p.ChangeDutyCycle(dc)
			time.sleep(0.5)
			
			dc=100
			p.ChangeDutyCycle(dc)
			time.sleep(0.5)

			time.sleep(0.0001)
			if GPIO.input(button_pin)==1:
				break
			
	else:
		p.ChangeDutyCycle(0)
		print("LED OFF!")
		
	light_on = not light_on	

	
GPIO.add_event_detect(button_pin, GPIO.RISING, callback=button_callback, bouncetime=50)

while 1:
	time.sleep(0.1)
	
p.stop()	
GPIO.cleanup()
