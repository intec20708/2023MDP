from picamera import PiCamera
import RPi.GPIO as GPIO
from time import sleep

# Set up GPIO
GPIO.setmode(GPIO.BCM)
pedal_pin = 17  # Change this to the GPIO pin your foot pedal is connected to
GPIO.setup(pedal_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Create a PiCamera object
camera = PiCamera()

def capture_image(channel):
    print("Foot pedal pressed! Capturing image...")
    
    # Capture an image
    camera.capture('foot_pedal_image.jpg')
    
    print("Image captured!")

# Set up event detection for the foot pedal press
GPIO.add_event_detect(pedal_pin, GPIO.FALLING, callback=capture_image, bouncetime=300)

try:
    print("Waiting for foot pedal press...")
    while True:
        sleep(1)  # Keep the script running

except KeyboardInterrupt:
    print("Cleaning up GPIO and exiting...")
    GPIO.cleanup()
    camera.close()
