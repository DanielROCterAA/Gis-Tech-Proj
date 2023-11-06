
import time
import sys
import requests
from fhict_cb_01.custom_telemetrix import CustomTelemetrix

com_port = "COM8"
TimeDisplay = [10, 11]
IndexInfo = "Baker Online.\nIndex:\nRed = No activity,\nYellow = active baking,\nGreen = baking Finished"

RedLed = 4
GreenLed = 5
YellowLed = 7
BtnLeft = 0
BtnRight = 0
BakeLVL = 0
InfoLVL = 0
SecurityLVL = 0

def StartBaking():
    #start a small time Loop as the 'baking' start
    global TimerValue
    board.displayShow(TimerValue)
    TimerValue -= 1
    time.sleep(0.5)
    
def initialDisplay():
    #setup display
    board.digital_write(TimeDisplay[0], 1)
    board.digital_write(TimeDisplay[1], 0)
  
   
def BtnSetup():
    #Sets the buttons Left & Right wit
    global BtnLeft
    global BtnRight
    BtnRight = board.digital_read(8)
    BtnLeft = board.digital_read(9)

def SendingStatus():
    #sends the signal to function
    LocalSignal = {'SignalVal' : 1}
    localSignal = requests.post('http://127.0.0.1:5000/', json = LocalSignal)
    if localSignal.status_code == 200:
        print("Status_Sending")
    else:
        print("Status_Sending Failed", localSignal.statstatus_code)

def Exiting():
    #clears all the output signals
    board.displayClear()
    board.digital_write(RedLed, 0)
    board.digital_write(GreenLed, 0)
    board.digital_write(YellowLed, 0)
def setup():
    #base Setup
    global board
    board = CustomTelemetrix(com_port)
    
    board.set_pin_mode_analog_output(RedLed)
    board.set_pin_mode_analog_output(GreenLed)
    board.set_pin_mode_analog_output(YellowLed)
    board.set_pin_mode_digital_input_pullup(8)
    board.set_pin_mode_digital_input_pullup(9)
     
    requests.post('http://127.0.0.1:5000/', json = {'SignalVal': 0})
    print(IndexInfo + "\nif you want display the index again press the right button for the index info.\nGood luck baking")
    initialDisplay()
 
def loop():
    board.digital_write(RedLed, 1)
    global BakeLVL
    global InfoLVL
    global SecurityLVL
    BtnSetup()
  
    if BtnRight:
        InfoLVL = BtnLeft[0]
        print(InfoLVL)
    if BtnLeft:
        BakeLVL = BtnLeft[0]
    

    if BakeLVL == 0 and SecurityLVL == 1:

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
                #sends the signal flask site
                SendingStatus()
                time.sleep(3)
                break
                
        board.digital_write(GreenLed, 0)

    if InfoLVL == 0 and SecurityLVL == 1:

        print(IndexInfo)
    SecurityLVL = 1
    time.sleep(0.2)

#-------Executeing Program-----
setup()
while True:
        try:
            loop()
        except KeyboardInterrupt:
            Exiting()
            print("Exiting")
            break
            
            
    