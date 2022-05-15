import time
import Adafruit_SSD1306
from PIL import Image, ImageDraw, ImageFont
import Adafruit_BMP.BMP085 as BMP085

disp = Adafruit_SSD1306.SSD1306_128_64(rst=None, i2c_address = 0x3C)

disp.begin()
disp.clear()
disp.display()

width = disp.width
height = disp.height
image = Image.new('1', (width, height))

draw = ImageDraw.Draw(image)
draw.rectangle((0,0,125,60), outline=255, fill=0)

x=8
padding=20
y=padding

font = ImageFont.load_default()
sensor = BMP085.BMP085()

while True:
	disp.clear()
	
	temp=sensor.read_temperature()
	pressure=sensor.read_pressure()
	altitude=sensor.read_altitude()
	
	print('Temp = {0:0.2f} *C'.format(temp))
	print('pressure = {0:0.2f} Pa'.format(pressure))
	print('altitude = {0:0.2f} m'.format(altitude))
	
	draw = ImageDraw.Draw(image)
	draw.rectangle((0,0,125,60), outline=255, fill=0)
	
	draw.text((x,y), 'Temp = {0:0.2f} *C'.format(temp), font=font, fill=255)
	draw.text((x,y + 8), 'pres = {0:0.2f} Pa'.format(pressure), font=font, fill=255)
	draw.text((x,y + 16), 'alti = {0:0.2f} m'.format(altitude), font=font, fill=255)
	
	disp.image(image)
	disp.display()
	
	time.sleep(2)
	
	
