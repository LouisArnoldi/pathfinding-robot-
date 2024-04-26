import time
import board
import adafruit_hcsr04
import pwmio
from adafruit_motor import servo, motor
import digitalio
import neopixel

# Init ultrasonic sensor module
sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.GP3, echo_pin=board.GP2)

# Initialize DC motors
m1a = pwmio.PWMOut(board.GP8, frequency=50)
m1b = pwmio.PWMOut(board.GP9, frequency=50)
motor1 = motor.DCMotor(m1a, m1b)
m2a = pwmio.PWMOut(board.GP10, frequency=50)
m2b = pwmio.PWMOut(board.GP11, frequency=50)
motor2 = motor.DCMotor(m2a, m2b)

# Initialize buttons
btn1 = digitalio.DigitalInOut(board.GP20)
btn2 = digitalio.DigitalInOut(board.GP21)
btn1.direction = digitalio.Direction.INPUT
btn2.direction = digitalio.Direction.INPUT
btn1.pull = digitalio.Pull.UP

# Initialize Neopixel RGB LEDs
RGB = neopixel.RGB
num_pixels = 2
pixels = neopixel.NeoPixel(board.GP18, num_pixels, brightness=0.02, auto_write=True, pixel_order=RGB)

def stop():
    motor1.throttle = 0
    motor2.throttle = 0

def backward(speed):
    motor1.throttle = -speed
    motor2.throttle = -speed

def forward(speed):
    motor1.throttle = speed
    motor2.throttle = speed

def lspin(speed):
    motor1.throttle = speed
    motor2.throttle = -speed

def rspin(speed):
    motor1.throttle = -speed
    motor2.throttle = speed

def lturn(speed):
    motor1.throttle = 0
    motor2.throttle = -speed

def rturn(speed):
    motor1.throttle = -speed
    motor2.throttle = 0

# set colors on LED
setColor = 0
pixels.fill((66, 255, 0))

def move_testing_forward():
    pixels.fill((255, 142, 0))
    print("call function")
    forward(0.5)
    time.sleep(2.5)
    stop()
    pixels.fill((66, 255, 0))

def move_testing_spin():
    #pixels.fill((255, 142, 0))
    print("call function")
    lspin(0.5)
    time.sleep(2.5)
    stop()
    rspin(0.5)
    time.sleep(2.5)
    stop()
    pixels.fill((66, 255, 0))

# you can call the function in the loop to log all distance values from the sensor
def catch_distance_value():
    try:
        print((sonar.distance,))
    except RuntimeError:
        print("Retrying!")
        pass

print("load py script")

# FOREVER LOOP
while True:
    if not btn1.value:  # if button 1 pressed call a function
        move_testing_forward()
    if not btn2.value:  # if button 2 pressed call a function
        move_testing_spin()

    if sonar.distance < 10:
        backward(0.2)
        time.sleep(0.5)
        stop()

    time.sleep(0.1)