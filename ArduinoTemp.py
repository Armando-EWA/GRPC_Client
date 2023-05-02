import sys
import serial
from serial import SerialException
import time
from loguru import logger
import re
import PortScanner

logger.debug("ArduinoTemp.py Started")

# Set Variables
global port
baud = 9600


def findArduinoPort():
    PortScanner.scanPorts()

    textfile = open('Logs/PortScanner.txt', 'r')
    readFile = textfile.read()
    textfile.close()
    # Looking in file and searching for REGEX FINDER: USB VID:PID=1A86:7523 SER= LOCATION=1-2.2 - COM: COM6
    # If "VID:PID=1A86:7523" is found, store it in group HWID, or group(1)
    # If "COM: " is found, then store the values requested(.+) and store in group(2)
    arduinoRegex = re.search(r'VID:PID=(?P<HWID>1A86:7523) .+COM: (?P<COM>.+)', readFile)

    logger.debug(arduinoRegex)
    if arduinoRegex:
        var_hwid = arduinoRegex.group(1)
        var_com = arduinoRegex.group(2)
        logger.debug(var_hwid)
        logger.debug(var_com)
        # Arduino Nano HWID Output: REGEX FINDER: USB VID:PID=1A86:7523 SER= LOCATION=1-2.2 - COM: COM6
        # If hwid matches 1A86:7523, then we know that is the Arduino Nano
        if var_hwid == "1A86:7523":
            logger.debug("Match")
            global port
            # Set the port to the regex capture which was COM: COM6
            port = var_com
        else:
            logger.debug("No Match")


def openArduinoSerial():
    while True:
        try:
            logger.debug("Attempting to open Arduino Serial Port...")
            time.sleep(2)

            ser = serial.Serial(port=port, baudrate=baud)
            logger.debug("Connected to Arduino Port using port: " + port)
            while ser.isOpen():
                if ser.inWaiting() > 0:
                    # read the bytes and convert from binary array to UTF-8
                    data_str = ser.read(ser.inWaiting()).decode('utf-8')
                    # print the incoming string without putting a new-line('\n') automatically after every print()
                    # print(data_str, end='')
                    pattern = r'Humidity: (?P<Humidity>\d+.\d+)%, Temp: (?P<Temp>\d+.\d+)'

                    # Search regex Pattern
                    data_str = re.search(pattern, data_str)

                    # If regex pattern is found, Humidity is group 1 and Temp is group 2.
                    if data_str:
                        humidity = data_str.group(1)
                        temp = data_str.group(2)
                        logger.debug("Regex Pattern Found. -- Humidity: " + data_str.group(1)
                                     + " Temperature: " + data_str.group(2))
                        # Optional, but recommended: sleep 10 ms (0.01 sec) once per loop to let
                        # other threads on your PC run during this time.
                        time.sleep(0.01)
        except SerialException as e:
            logger.debug("Error: " + str(e))
            time.sleep(2)


if __name__ == "__main__":
    findArduinoPort()
    openArduinoSerial()
