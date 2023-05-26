"""
Req: I2C is enables with raspi-config.
Req: Adafruit CircuitPython SHT4x library.
 pip3 install adafruit-circuitpython-sht4x
Req: Adafruit Adafruit_Blinka library.
Req: Adafruit CircuitPython MAX31865 library.
 pip3 install adafruit-circuitpython-max31856
Req: Running at least Python 3.0.
I2C is used to communicate with the Adafruit SHT40 temp
 and humidity sensor located in the electronics box. (0x44).
SPI is used to communicate with the 2x Adafruit MAX31856 Thermocouple DACs.
"""

"""                                                 Relay                                   Binary to Int
        Mode        Setting                         N2  O2  F   Bypass, Boiler, Heater
    00  OFF         No Furnace, N2                  0   0   0   0                           0
    01  OFF, PH     No Furnace, Wet O2              0   0   0   1  (pre-heat mode)          1
    02  OFF         No Furnace, Dry O2              0   0   0   0                           0   
    10  F1, N2      Top Furnace, N2 Gas             1   0   0   0                           8
    11  F1, Wet     Top Furnace, Wet O2             0   1   0   1                           5
    12  F1, Dry     Top Furnace, Dry O2             0   1   0   0                           4
    20  F2, N2      Bottom Furnace, N2 Gas          1   0   1   0                           10
    21  F2, Wet     Bottom Furnace, Wet O2          0   1   1   1                           7
    22  F2, Dry     Bottom Furnace, Dry O2          0   1   1   0                           6
    
    31  F1, N2+     Top Furnace, N2 + Preheat       1   0   0   1                           9
    41  F2, N2+     Bottom Furnace, N2 + Preheat    1   0   1   1                           11
"""




# Library Imports
import signal
import sys
import RPi.GPIO as GPIO
import board
import digitalio
import adafruit_max31856
import adafruit_sht4x
from bitarray import bitarray
import time

## Define key parameters for control
triggerN2 = 300     ## degrees Celsius
triggerO2 = 1000    ## degrees Celsius

fluidRelays = bitarray(4)    ## 3 2 1 0 ::  [Bubbler, Heaterwrap, DirB], DirF, N2, O2

commandMode = 0
desiredMode = 0
operationMode = 0

## Define User Interface Input Pins
selectPins = [0, 11, 26, 1] ## wet02, dry02, top furnace, bottom furnace
for pin in selectPins:
    GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)

rotaryPins = [16, 20, 21]   ## Rotary Encoder A, B, Select

## Define Sensor Input Pins
inputLevel = 10     ## water level low float
inputPresN2 = 5     ## nitrogen pressure switch correlates to good flow
inputPresO2 = 19    ## oxygen ...
# SDAHum = 6        ## SDA for i2c(1) communication with SHT40 Temp/Hum Sensor
# SCLHum = 13       ## SCL for i2c(1) ...

## Define Outputs
relayPins = [2, 3, 4, 17, 27, 22, 0, 9] ## H20, O2, N2, DirB, DifF, Heater, Bubbler, Fans
for pin in relayPins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)

def user_selection_callback(pinNum):
    pass

def encoder_callback(channel):
    pass

def sensor_callback(channel):
    pass

def kill_relays()
    pass

def mode_check():
    checkDry = GPIO.input(inputDry)
    checkWet = GPIO.input(inputWet)
    checkF1 = GPIO.input(inputFurn1)
    checkF2 = GPIO.input(inputFurn2)
    result = (checkWet + 2 * checkDry + (checkF1 + 2 * checkF2) * 10)
    return  result

def check_temps():
    f1Temp = furnace1temp.temperature
    f2Temp = furnace2temp.temperature
    return f1Temp, f2Temp

def pickOperation(operationMode, desiredMode, F1Temp, F2Temp):
    if operationMode == 0:
        newMode = temperatureControlled(desiredMode, F1Temp, F2Temp)
        return newMode
    elif operationMode == 1:
        commandRelays(desiredMode)
        newMode = desiredMode
        return newMode
    else:
         return "Error"

def temperatureControlled(desiredMode, F1Temp, F2Temp):
    if desiredMode == 0 or desiredMode == 2:
        # No Furnace, N2
        commandRelays(0) # off
        return 0

    elif desiredMode == 1:
        # No Furnace, Preheat
        commandRelays(desiredMode)
        return desiredMode

    elif desiredMode == 2:
        # No Furnace, Dry O2
        commandRelays(desiredMode)
        return desiredMode

    elif desiredMode == 10:
        # Upper Furnace, N2 Only
        if F1Temp < triggerN2:
            commandRelays(2)
            return 2
        else:
            commandRelays(desiredMode)
            return desiredMode

    elif desiredMode == 11:
        # Upper Furnace, Wet O2
        if F1Temp <= triggerN2:
            commandRelays(1) # preheat
            return 1
        elif triggerN2 < F1Temp <= triggerO2: # flow N2 while still preheating
            commandRelays(13)
            return 13
        else:
            commandRelays(desiredMode)
            return desiredMode

    elif desiredMode == 12:
        # Upper furnace, Dry O2
            if F1Temp <= triggerN2:
                commandRelays(0)  # Off
                return 0
            elif triggerN2 < F1Temp <= triggerO2:
                commandRelays(10) # Top Furnace, N2
                return 10
            else:
                commandRelays(desiredMode)
                return desiredMode

    elif desiredMode == 20:
        # Bottom Furnace, N2 Only
        if F2Temp < triggerN2: # off
            commandRelays(0)
            return 0
        else:
            commandRelays(desiredMode)
            return desiredMode

    elif desiredMode == 21:
        # Bottom Furnace, Wet O2
            if F2Temp <= triggerN2:
                commandRelays(1)  # preheat
                return 1
            elif triggerN2 < F2Temp <= triggerO2:  # flow N2 bottom while still preheating
                commandRelays(23)
                return 23
            else:
                commandRelays(desiredMode)
                return desiredMode

    elif desiredMode == 22:
        # Bottom Furnace, Dry O2
            if F2Temp <= triggerN2:
                commandRelays(0)  # Off
                return 0
            elif triggerN2 < F2Temp <= triggerO2:  # flow N2 bottom furnace
                commandRelays(20)
                return 20
            else:
                commandRelays(desiredMode)
                return desiredMode
def commandRelays(commandMode):




    ## Nitrogen on/off
    if commandMode == 10 or 20 or 13:
        GPIO.output(relayN2, GPIO.HIGH)
    else:
        GPIO.output(relayN2, GPIO.LOW)

    ## O2 on off
    if commandMode == 11 or 12 or 21 or 22:
        GPIO.output(relayO2, GPIO.HIGH)
    else:
        GPIO.output(relayN2, GPIO.LOW)

    ## Furnace 2 Diverter
    if commandMode > 19:
        GPIO.output(relayDirF, GPIO.HIGH)
    else:
        GPIO.output(relayDirF, GPIO.LOW)

    ## bubbler, heater, bubbler diverter
    if commandMode % 10 == 1 or commandMode == 13 or commandMode == 23:
        GPIO.output(relayDirB, GPIO.HIGH)
        GPIO.output(relayHeater, GPIO.HIGH)
        GPIO.output(relayBubbler, GPIO.HIGH)
    else:
        GPIO.output(relayDirB, GPIO.LOW)
        GPIO.output(relayHeater, GPIO.LOW)
        GPIO.output(relayBubbler, GPIO.LOW)

def waterFill_callback():
    waterLevel = GPIO.input(inputWet)
    if waterLevel == 1:
        GPIO.output(relayH2O, GPIO.HIGH)
    else:
        GPIO.output(relayH2O, GPIO.LOW)
    return waterLevel

if __name__ == '__main__':
    # Configuration settings
    GPIO.setmode(GPIO.BCM)
    i2c = board.I2C()  # initialize I2C
    spi = board.SPI()  # initialize SPI
    cs1 = digitalio.DigitalInOut(board.D5)  # !!!! change pin # SPI CS pin furnace temp 1
    cs2 = digitalio.DigitalInOut(board.D6)  # !!!! change pin # SPI CS pin furnace temp 2
    cs1.direction = digitalio.Direction.OUTPUT
    cs2.direction = digitalio.Direction.OUTPUT
    furnace1temp = adafruit_max31856.MAX31856(spi, cs1)
    furnace2temp = adafruit_max31856.MAX31856(spi, cs2)
    TempHum = adafruit_sht4x.SHT4x(board.I2C())  # initialize SHT40
    # print("Found SHT4x with serial number", hex(sht.serial_number))

    ##def init_gpio()
    GPIO.setup(inputWet, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(inputDry, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(inputLevel, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(inputPresO2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(inputPresN2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(inputA, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(inputB, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(inputS, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    GPIO.setup(relayFans, GPIO.OUT)
    GPIO.setup(relayHeater, GPIO.OUT)
    GPIO.setup(relayDirF, GPIO.OUT)
    GPIO.setup(relayDirB, GPIO.OUT)
    GPIO.setup(relayH2O, GPIO.OUT)
    GPIO.setup(relayN2, GPIO.OUT)
    GPIO.setup(relayO2, GPIO.OUT)

    # event ISR setup
    GPIO.add_event_detect(inputWet, GPIO.BOTH, user_selection_callback, bouncetime = 100)
    GPIO.add_event_detect(inputDry, GPIO.BOTH, user_selection_callback, bouncetime=100)
    GPIO.add_event_detect(inputFurn1, GPIO.BOTH, user_selection_callback, bouncetime=100)
    GPIO.add_event_detect(inputFurn2, GPIO.BOTH, user_selection_callback, bouncetime=100)
    GPIO.add_event_detect(inputS, GPIO.FALLING, user_selection_callback, debounce = 100)
    GPIO.add_event_detect(inputA, GPIO.BOTH, encoder_callback, bouncetime = 15)
    GPIO.add_event_detect(inputB, GPIO.BOTH, encoder_callback, bouncetime = 15)
    GPIO.add_event_detect(inputPresN2, GPIO.BOTH, sensor_callback, debouce=1000)
    GPIO.add_event_detect(inputPresO2, GPIO.BOTH, sensor_callback, debouce=1000)
    GPIO.add_event_detect(inputLevel, GPIO.BOTH, waterFill_callback, debouce=1000)

    # system defaults


    # main loop
    while True:
        #F1Temp, F2Temp = system_check()
        F1Temp = 100
        F2Temp = 125
        pickOperation(operationMode, desiredMode, F1Temp, F2Temp)
