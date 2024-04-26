# robotOS

## BEFORE STARTING

The robot need batterys or LiPo to work all servos and sensors. The USB connection can't be used 
for energy transmittion and is only for data connection.

## LOADING ALL FILES & SERVICES

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

## ISSUES

[x] change names of moving directions
[ ] first tests of us sensor ("if distance under 10 then stop driving)


