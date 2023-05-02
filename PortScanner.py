#!/usr/bin/python

import sys
import serial.tools.list_ports
from loguru import logger
import time


# While this program is intended for Windows, let's just verify
def checkOS():
    logger.debug("Checking System Platform...")
    time.sleep(1)
    if sys.platform.startswith('win'):
        logger.debug("System Platform detected: " + sys.platform)
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        logger.debug("System Platform detected: " + sys.platform)
    elif sys.platform.startswith('darwin'):
        logger.debug("System Platform: " + sys.platform)
    else:
        raise EnvironmentError('Unsupported platform')


def scanPorts():
    time.sleep(1)
    logger.debug("Scanning port comports...\n")
    try:
        ports = serial.tools.list_ports.comports()
        if ports:
            i = 0  # Counter for Port count
            time.sleep(1)
            logger.debug("Ports Found:")
            logger.debug("-------------")
            time.sleep(1)
            # Open File to write Port Information to Regex Later
            PortScanner_File = open('Logs/PortScanner.txt', 'w')
            # For each port found, print it
            for port, desc, hwid in sorted(ports):
                i += 1  # Increase by 1 for every iteration
                logger.debug("Port: " + port)
                logger.debug("Description: " + desc)
                logger.debug("Hardware Information: " + hwid)
                logger.debug("Port " + str(i) + ": " + hwid + " - COM: " + port)
                PortScanner_File.write("Port " + str(i) + ": " + hwid + " - COM: " + port + "\n")
                logger.debug("-------------")
                time.sleep(1)
            # Close File
            PortScanner_File.close()
        else:
            logger.debug("No serial ports found...")
    except Exception as e:
        logger.debug(e)


if __name__ == "__main__":
    time.sleep(1)
    logger.debug("Starting Port Scanner..")
    # Check OS being used
    checkOS()
    # Scan ports
    scanPorts()

    time.sleep(2)
    logger.debug("Exiting Program..")
    time.sleep(3)
