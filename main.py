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

# Initialize sound module
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


# connect motor controller to PINS
move = MotorController(board.GP8, board.GP9, board.GP10, board.GP11)


# frequently used robot functions

def play_tone(frequency, duration):
    tone = simpleio.tone(PIEZO_PIN, frequency, duration=duration)
    return tone


def move_and_stop(direction, duration):
    direction(0.5)
    time.sleep(duration)
    move.stop()


# functions that are called up by pressing a button or by an error

def pathfinding():
    print("pathfinding session started")
    while True:
        obstacle = sonar.distance < 13
        try:
            print("run pathfinding")
            if obstacle:
                # backwards and update position
                move_and_stop(move.backward, 0.4)
                print("distance < 20, turn left")
                # change the angle left
                move_and_stop(move.lspin, 0.4)
                sensor_data_left = sonar.distance
                print("distance < 20, turn right")
                # change the angle right
                move_and_stop(move.rspin, 0.8)
                sensor_data_right = sonar.distance
                if sensor_data_right < 13 or sensor_data_left < 13:
                    print("can't driving yet")
                    error_mode()
                    break
                elif sensor_data_left > sensor_data_right:
                    play_tone(262, 0.1)
                    move_and_stop(move.lspin, 0.8)
                    move_and_stop(move.forward, 0.3)
                elif sensor_data_right > sensor_data_left:
                    play_tone(659, 0.1)
                    move_and_stop(move.forward, 0.3)
            if not obstacle:
                print("drive forward no obstacle detected")
                move_and_stop(move.forward, 0.3)
                move_and_stop(move.lspin, 0.1)
                time.sleep(0.2)
                sensor_data_left = sonar.distance
                move_and_stop(move.rspin, 0.2)
                time.sleep(0.2)
                sensor_data_right = sonar.distance
                if sensor_data_left > sensor_data_right:
                    play_tone(262, 0.1)
                    move_and_stop(move.lspin, 0.4)
                    move_and_stop(move.forward, 0.3)
                if sensor_data_right > sensor_data_left:
                    play_tone(659, 0.1)
                    move_and_stop(move.forward, 0.3)
        except RuntimeError:
            move.stop()
            error_mode()
            break


def error_mode():
    print("error mode")
    play_tone(659, 0.1)
    pixels.fill((255, 255, 0))
    pixels.show()
    time.sleep(0.2)  # Wait for 1 second
    play_tone(262, 0.1)
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
    pixels.fill((66, 255, 0))
    pixels.show()
    # Button 1: pathfinding mode
    if not btn1.value:
        pathfinding()
    # Button 2: test mode
    if not btn2.value:
        test_mode()
    time.sleep(0.1)  # is needed to refresh buttons
