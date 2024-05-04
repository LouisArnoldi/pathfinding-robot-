# pathfinding robot car using CircuitPython

A self-made two-wheeled robot car, that autonomously completes a test course with pathfinding.

![Hey robot :)](img%2FD171A1F1-F882-466D-B948-9D386C752012.GIF)

## Project setup

* Chassis/wheels/servos: MBot 
* Mainboard: Maker Pi RP2040 with Raspberry Pi Pico
* Sensor: ultrasonic sensor HC-SR04
* Based on CircuitPython

## Batteries

The robot need batteries or LiPo to work all servos and sensors. The USB connection can't be used 
for energy transmission and is only for data connection.

## Prepare the robot 

### load CIRCUITPY
it is not necessary to load files manually. if there are not loaded from root file path, refresh with 
"Reload from Disk". Sometimes the robot must be reboot to show all files and the screen

### load REPL 
write in Terminal: 
screen /dev/ttyACM0 115200

### load libraries to lib folder on CircuitPython drive
load bundle from this source: https://github.com/adafruit/Adafruit_CircuitPython_Bundle/releases/tag/20240417
extract adafruit-circuitpython-bundle-9.x-mpy-20240417.zip 
For the HCSR04 - You'll want to copy the necessary libraries from the bundle to your lib folder on your CIRCUITPY drive:

    adafruit_hcsr04.mpy
    adafruit_bus_device

## run pathfinding 
* press the switch to start
* start the pathfinding mode with button GP20/BTN1
* GP21/BTN2 calls the test mode (not in use)

