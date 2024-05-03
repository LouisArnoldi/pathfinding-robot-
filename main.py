import time
import board
import adafruit_hcsr04
import pwmio
from adafruit_motor import servo, motor
import digitalio
import neopixel
import simpleio

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
btn2.pull = digitalio.Pull.UP

# Initialize Neopixel RGB LEDs
RGB = neopixel.RGB
num_pixels = 2
pixels = neopixel.NeoPixel(board.GP18, num_pixels, brightness=0.02, auto_write=False)

# Define sound module
PIEZO_PIN = board.GP22

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

def pathfinding():
    print("pathfinding session started")
    position = 0

    while True:
        obstacle = sonar.distance < 13
        print((sonar.distance, ))

        try:
            print("run pathfinding")
            if obstacle and position == 0:
                # backwards and update position
                backward(0.5)
                time.sleep(0.4)
                stop()
                print("distance < 20, turn left")
                # change the angle left
                lspin(0.5)
                time.sleep(0.4)
                stop()
                sensor_data_left = sonar.distance
                print("distance < 20, turn right")
                # change the angle right
                rspin(0.5)
                time.sleep(0.8)
                stop()
                sensor_data_right = sonar.distance
                if sensor_data_right < 13 or sensor_data_left < 13:
                    print("can't driving yet")
                    error_mode()
                    break
                elif sensor_data_left > sensor_data_right:
                    simpleio.tone(PIEZO_PIN, 262, duration=0.1)
                    lspin(0.5)
                    time.sleep(0.8)
                    stop()
                    position = 0
                    forward(0.5)  # drive forward with half power
                    time.sleep(0.3)  # drive length
                    stop()
                elif sensor_data_right > sensor_data_left:
                    simpleio.tone(PIEZO_PIN, 659, duration=0.1)
                    position = 0
                    forward(0.5)  # drive forward with half power
                    time.sleep(0.3)  # drive length
                    stop()
            if not obstacle:
                print("drive forward no obstacle detected")
                position = 0
                forward(0.5)  # drive forward with half power
                time.sleep(0.3)  # drive length
                stop()
                lspin(0.5)
                time.sleep(0.1)
                stop()
                time.sleep(0.2)
                sensor_data_left = sonar.distance
                rspin(0.5)
                time.sleep(0.2)
                stop()
                time.sleep(0.2)
                sensor_data_right = sonar.distance
                if sensor_data_left > sensor_data_right:
                    simpleio.tone(PIEZO_PIN, 262, duration=0.1)
                    lspin(0.5)
                    time.sleep(0.4)
                    stop()
                    position = 0
                    forward(0.5)  # drive forward with half power
                    time.sleep(0.3)  # drive length
                    stop()
                if sensor_data_right > sensor_data_left:
                    simpleio.tone(PIEZO_PIN, 659, duration=0.1)
                    position = 0
                    forward(0.5)  # drive forward with half power
                    time.sleep(0.3)  # drive length
                    stop()
        except:
            stop()
            error_mode()
            break

def error_mode():
    print("error mode")

    simpleio.tone(PIEZO_PIN, 659, duration=0.15)

    pixels.fill((255, 255, 0))
    pixels.show()
    time.sleep(0.2)  # Wait for 1 second

    simpleio.tone(PIEZO_PIN, 262, duration=0.1)

    # Fill pixels with red color
    pixels.fill((255, 0, 0))
    pixels.show()
    time.sleep(0.2)  # Wait for 1 second

def test_mode():
    # you can call the function to log all distance values from the sensor
    try:
        print((sonar.distance,))
    except RuntimeError:
        print("Retrying!")
        pass

print("device is ready")

# FOREVER LOOP
while True:
    # set colors on LED
    setColor = 0  # is this variable unnecessary?
    pixels.fill((66, 255, 0))
    pixels.show()

    # Button 1: pathfinding mode
    if not btn1.value:
        pathfinding()
    # Button 2: test mode
    if not btn2.value:
        test_mode()

    time.sleep(0.1)