
import time
import sys
from fhict_cb_01.custom_telemetrix import CustomTelemetrix


def setup():
    global board
    board = CustomTelemetrix(com_port = "COM8")

def loop():

   
    pass

setup()
while True:
        try:
            loop()
        except KeyboardInterrupt:
            print("Exiting")
            board.shutdown()
            sys.exit()
    