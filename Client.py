import time
import grpc
import greeting_pb2
import greeting_pb2_grpc

import threading
import ArduinoTemp
from datetime import date

today = date.today()
ArduinoTemp.findArduinoPort()


def ArduinoThread():
    ArduinoTemp.openArduinoSerial()


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = greeting_pb2_grpc.GreeterStub(channel)
        response = stub.greet(greeting_pb2.ClientInput(name='John', greeting="I am happy."))
        send = stub.greet(greeting_pb2.ClientInput(name='Bill', greeting="I am sad."))
    print("Greeter client received following from server: " + response.message)
    print("Greeter client received following from server: " + send.message)


def timer():
    # created a global variable.

    # where 5 is the number of seconds to wait
    threading.Timer(5, timer).start()
    # running the main function
    run()


timer()
ArduinoThread()
