
import time, sys
from flask import Flask
from fhict_cb_01.custom_telemetrix import CustomTelemetrix

com_port = "COM8"
TimeDisplay = [10, 11]

RedLed = 4
GreenLed = 5
YellowLed = 7
security = 0
level = 0
preLvl = 0 
BtnLeft = 0
BtnRight = 0


Web = Flask(__name__)


    
if __name__ == "__main__":
    pass
def StartBaking():
    global TimerValue
    board.displayShow(TimerValue)
    TimerValue -= 1
    time.sleep(0.5)
    

def initialDisplay():

    board.digital_write(TimeDisplay[0], 1)
    board.digital_write(TimeDisplay[1], 0)



def BtnSetup():
    global BtnLeft
    global BtnRight
    BtnRight = board.digital_read(8)
    BtnLeft = board.digital_read(9)
   

def setup():
    
    global board
    board = CustomTelemetrix(com_port)
    
    #looks at button for any change press in or out as ann output
    #board.set_pin_mode_digital_input_pullup(9, callback = BtnChange)
    #this with board digital read out the btn status with 1 being on and 0 pressed, make sure you [0] the value output to get the 1/0 
    #board.set_pin_mode_digital_input_pullup(8)

    board.set_pin_mode_analog_output(RedLed)
    board.set_pin_mode_analog_output(GreenLed)
    board.set_pin_mode_analog_output(YellowLed)
    board.set_pin_mode_digital_input_pullup(8)
    board.set_pin_mode_digital_input_pullup(9)

    initialDisplay()
    

    



def loop():
    board.digital_write(RedLed, 1)
    global level
    global security
    BtnSetup()
    if BtnLeft:
        level = BtnLeft[0]
        print(level)

    if level == 0 and security == 1:

        print("hit")
        board.digital_write(RedLed, 0)
        global TimerValue
        TimerValue = 60

        while True:
            board.digital_write(YellowLed, 1)
            StartBaking()
            if TimerValue == -1:
                board.digital_write(YellowLed, 0)
                board.digital_write(GreenLed, 1)
                time.sleep(3)
                #sent signal to oder
                break

        board.digital_write(GreenLed, 0)

    security = 1
    time.sleep(1)

    
    
def Exiting():
    board.displayClear()
    board.digital_write(RedLed, 0)
    board.digital_write(GreenLed, 0)
    board.digital_write(YellowLed, 0)
def dumpster():
    while True:
            global i
            i += 1
            print(i)
            if i == 10:
                i = 0
                break
    localStatus = board.digital_read(8)
  
    if localStatus:
        preLvl = localStatus[0]
        print(preLvl)
        time.sleep(0.2)
        if preLvl == 0:
            print("hit")

    else:
        print("no signal")

    #default kit
    countDownVal = 60
    time.sleep(0.2)
    while(countDownVal == 0):
        print(countDownVal)   
        Timer(countDownVal)
        time.sleep(1)
        countDownVal = countDownVal - 1

setup()
while True:
        try:
            loop()
        except KeyboardInterrupt:
            Exiting()
            print("Exiting")
            sys.exit()
            board.shutdown()
            
            
    