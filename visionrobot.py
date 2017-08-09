import RPi.GPIO as GPIO
import time
import os
import picamera
import io
from google.cloud import vision
import BlynkLib

BLYNK_AUTH = '4d83fa21689b4ab0bffa99055763cdcb'

# Initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH)

GPIO.setmode(GPIO.BOARD)
GPIO.cleanup()
TRIG = 36
ECHO = 32

def kald_google():
    print('foer kald til billede')
    camera = picamera.PiCamera()
    camera.vflip = True
    camera.hflip = True
#Set camera to black and white
#camera.color_effects = (128,128)
    print('efterr camera def')
    camera.capture('image.jpg')
    print('tag et billede')


    print('foer visionclient')
    vision_client = vision.Client()
    print('Foer filen')
    file_name = 'image.jpg'
    print('Inden kald til google')
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()
        image = vision_client.image(
            content=content, )
#    labels = image.detect_logos()
    labels = image.detect_labels()
    for label in labels:
        print(label.description, label.score)



#kald_google()

def distance():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)

    GPIO.output(TRIG, True)
    time.sleep(0.0001)
    GPIO.output(TRIG, False)

    while GPIO.input (ECHO) == False:
        start = time.time()

    while GPIO.input( ECHO) == True:
        end = time.time()

    sig_time = end-start

    distance = sig_time / 0.000058

    print('Distance: {} cm' .format(distance))

    GPIO.cleanup()

    return distance



def setup():
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(12, GPIO.OUT)
    GPIO.setup(16, GPIO.OUT)
    GPIO.setup(18, GPIO.OUT)
    GPIO.setup(22, GPIO.OUT)

#@blynk.VIRTUAL_WRITE(1)
def frem(t):
    setup()
    GPIO.output(18, False)
    GPIO.output(22, True)
    GPIO.output(12, True)
    GPIO.output(16, False)

    time.sleep(0.05)
    GPIO.cleanup()

#@blynk.VIRTUAL_WRITE(2)
def bag(t):
    setup()
    GPIO.output(22, False)
    GPIO.output(18, True)
    GPIO.output(16, True)
    GPIO.output(12, False)

    time.sleep(0.05)
    GPIO.cleanup()

#@blynk.VIRTUAL_WRITE(3)
def pivot_venstre(t):
    setup()
    GPIO.output(22, False)
    GPIO.output(16, False)
    GPIO.output(12, False)

    time.sleep(0.25)
    GPIO.cleanup()

#@blynk.VIRTUAL_WRITE(4)
def pivot_hoejre(t):
    setup()
    GPIO.output(18, False)
    GPIO.output(22, False)
    GPIO.output(12, True)
    GPIO.output(16, False)

    time.sleep(0.25)
    GPIO.cleanup()

# Start Blynk (this call should never return)
#blynk.run()
while True:
    dist = distance()
    time.sleep(0.05)

    if dist > 20:
        frem(1)
    elif 20 > dist > 3:
        bag(1)
    elif dist <= 3:
        GPIO.cleanup()
