import time
import board
import adafruit_hcsr04
import pwmio
from adafruit_motor import servo, motor
import digitalio
import neopixel
import simpleio

# Initialize ultrasonic sensor module
sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.GP3, echo_pin=board.GP2)

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


class MotorController:
    def __init__(self, m1a_pin, m1b_pin, m2a_pin, m2b_pin, frequency=50):
        self.motor1 = motor.DCMotor(pwmio.PWMOut(m1a_pin, frequency=frequency), pwmio.PWMOut(m1b_pin, frequency=frequency))
        self.motor2 = motor.DCMotor(pwmio.PWMOut(m2a_pin, frequency=frequency), pwmio.PWMOut(m2b_pin, frequency=frequency))

    def stop(self):
        self.motor1.throttle = 0
        self.motor2.throttle = 0

    def backward(self, speed):
        self.motor1.throttle = -speed
        self.motor2.throttle = -speed

    def forward(self, speed):
        self.motor1.throttle = speed
        self.motor2.throttle = speed

    def lspin(self, speed):
        self.motor1.throttle = speed
        self.motor2.throttle = -speed

    def rspin(self, speed):
        self.motor1.throttle = -speed
        self.motor2.throttle = speed

    def lturn(self, speed):
        self.motor1.throttle = 0
        self.motor2.throttle = -speed

    def rturn(self, speed):
        self.motor1.throttle = -speed
        self.motor2.throttle = 0


move = MotorController(board.GP8, board.GP9, board.GP10, board.GP11)


def pathfinding():
    print("pathfinding session started")

    while True:
        obstacle = sonar.distance < 13
        print((sonar.distance, ))

        try:
            print("run pathfinding")
            if obstacle:
                # backwards and update position
                move.backward(0.5)
                time.sleep(0.4)
                move.stop()
                print("distance < 20, turn left")
                # change the angle left
                move.lspin(0.5)
                time.sleep(0.4)
                move.stop()
                sensor_data_left = sonar.distance
                print("distance < 20, turn right")
                # change the angle right
                move.rspin(0.5)
                time.sleep(0.8)
                move.stop()
                sensor_data_right = sonar.distance
                if sensor_data_right < 13 or sensor_data_left < 13:
                    print("can't driving yet")
                    error_mode()
                    break
                elif sensor_data_left > sensor_data_right:
                    simpleio.tone(PIEZO_PIN, 262, duration=0.1)
                    move.lspin(0.5)
                    time.sleep(0.8)
                    move.stop()
                    move.forward(0.5)  # drive forward with half power
                    time.sleep(0.3)  # drive length
                    move.stop()
                elif sensor_data_right > sensor_data_left:
                    simpleio.tone(PIEZO_PIN, 659, duration=0.1)
                    move.forward(0.5)  # drive forward with half power
                    time.sleep(0.3)  # drive length
                    move.stop()
            if not obstacle:
                print("drive forward no obstacle detected")
                move.forward(0.5)  # drive forward with half power
                time.sleep(0.3)  # drive length
                move.stop()
                move.lspin(0.5)
                time.sleep(0.1)
                move.stop()
                time.sleep(0.2)
                sensor_data_left = sonar.distance
                move.rspin(0.5)
                time.sleep(0.2)
                move.stop()
                time.sleep(0.2)
                sensor_data_right = sonar.distance
                if sensor_data_left > sensor_data_right:
                    simpleio.tone(PIEZO_PIN, 262, duration=0.1)
                    move.lspin(0.5)
                    time.sleep(0.4)
                    move.stop()
                    move.forward(0.5)  # drive forward with half power
                    time.sleep(0.3)  # drive length
                    move.stop()
                if sensor_data_right > sensor_data_left:
                    simpleio.tone(PIEZO_PIN, 659, duration=0.1)
                    move.forward(0.5)  # drive forward with half power
                    time.sleep(0.3)  # drive length
                    move.stop()
        except:
            move.stop()
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
    # hold the button to log all distance values from the sensor
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