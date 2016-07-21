#TestingRig
#14 July 2016
#Nathan Stasin

import RPi.GPIO as GPIO
from time import sleep
import math #used for rounding up

GPIO.cleanup()

def Initialise():

    GPIO.setmode(GPIO.BCM)#BCM mode used for RPi cobbler breadboard breakout

    GPIO.setwarnings(False) #Turn off GPIO warnings

    #Rotary encoder
    #define pins as inputs
    GPIO.setup(20, GPIO.IN)#yellow wire, signal A. Pin 21
    GPIO.setup(21, GPIO.IN) #green wire, signal B. Pin 20

    #2 relay module : IN2 = green(forward LED) IN1 = red(backwards LED)
    #set pins as outputs
    GPIO.setup(24, GPIO.OUT)#Green LED(forward),white wire
##    GPIO.setup(23, GPIO.OUT) #Red LED (backwards),orange wire

    #Signal LED
    #Set pin as output
    GPIO.setup(18, GPIO.OUT) #Yellow LED signal light

    
    print "-----------------------------------"
    print "Shaft testing rig program running"
    sleep (0.5)
    print "-----------------------------------"

    #turn off all ouput pins
    GPIO.output(24, GPIO.HIGH)#turns off motor forward pin, green LED
##    GPIO.output(23, GPIO.HIGH)#turns off motor backward pin, red LED
    GPIO.output(18, GPIO.LOW)#turns off yellow signal LED

    #end of Initialise()
    return

def FlashSignalLight():
    
    for i in range(0,3):
        GPIO.output(18, GPIO.LOW)#turns on yellow signal LED
        sleep (0.2)
        GPIO.output(18, GPIO.HIGH)#turns off yellow signal LED
        sleep(0.2)

    GPIO.output(18, GPIO.LOW)#turns off yellow signal LED

    #end of FlashSignalLight
    return

def ReloadSettings():
    my_file = open("settings.txt", "r")#open the settings file
    
    #make variable ForwardDegrees accessible globally
    global ForwardDegrees
    #read and convert to integer
    ForwardDegrees = int(my_file.readline())
    
    global Cycles
    Cycles = int(my_file.readline())

    global SleepTime
    SleepTime = int(my_file.readline())
    
    print "----------------------"
    print "Settings from previous session: "
    print "----------------------"
    sleep(1)
    print "Forward Degrees = " + str(ForwardDegrees)
    print "Forward Cycles = " + str(Cycles)
    print "SleepTime = " +str(SleepTime)
    print "----------------------"
    sleep(1)

def GetUserInput():

    while True:
        
        #strings containing variety of possible responses for yes and no
        global yes
        global no
        yes = ["YES", "yes", "y", "Y", "Ye", "ye"]
        no = ["No", "NO", "no", "N"]

        #make AskUser response accessible globally
        global AskUser

        try:
            print "-----------------------------"
            AskUser = raw_input("Do you want to reload settings from last session? Enter Y or N: ")
            AskUser = AskUser.upper()#Make answer upper case
            if AskUser in yes:
                sleep(0.2)
                print "-----------------------------"
                print "Reloading settings from the last session"
                sleep(1)
                break
            elif AskUser in no:
                sleep(0.2)
                print "-----------------------------"
                print "You wish to enter a new batch of settings"
                sleep(0.3)
                print "If using numberpad on keyboard, make sure that NumLock is on"
                sleep(0.3)
                break
            else:
                sleep(0.2)
                print "Please respond yes or no"
                sleep(0.3)

        except:
           print "Please respond yes or no" 

    #end of GetUserInput

def LoadNewSettings():
    #User input with error handling
    Settings = [] #creates empty string called Settings

    while True:
        try:
            global ForwardDegrees
            ForwardDegrees = int(raw_input("Enter degrees to move forward: "))
            
            Settings.append(ForwardDegrees)#adds it to string called Settings
            sleep(0.1)
            break

        except ValueError:
            print "Please enter a number. Try again"
            sleep(0.3)

   
    while True:
        try:
            global Cycles
            Cycles = int(raw_input("Enter the desired number of forward cycles: "))
            
            Settings.append(Cycles)
            sleep(0.1)
            break

        except ValueError:
            print "Please enter a number. Try again"
            sleep(0.3)

    while True:
        try:
            global SleepTime
            SleepTime = int(raw_input("Enter the desired sleep time, in seconds: "))

            if SleepTime <3:
                sleep(1)
                print "You cannot sleep for less than 3 seconds."
                SleepTime = 3
            
            Settings.append(SleepTime)
            sleep(0.1)
            break

        except ValueError:
            print "Please enter a number. Try again"
            sleep(0.3)

    #Write to settings file
    
    my_file = open("settings.txt", "r+")

    for item in Settings:
        my_file.write(str(item) + "\n")

    my_file.close()

    print "----------------------"
    print "Your new settings"
    print "----------------------"
    print "Forward Degrees = " + str(ForwardDegrees)
    print "Cycles = " + str(Cycles)
    print "Sleep Time = " + str(SleepTime)
    print "----------------------"

    #End of LoadNewSettings

def MoveMotorForward():
    GPIO.output(24, GPIO.LOW) #turn on motor in forward direction (green LED)

def SwitchOffMotor():
    GPIO.output(24, GPIO.HIGH) #turn off motor in forward direction (green LED)

def PrintInfo():
    sleep(1)
    print "----------------------"
    print "Settings"
    print "    "
    print "Forward Degrees = " + str(ForwardDegrees)
    print "Cycles = " + str(Cycles)
    print "SleepTime = "+str(SleepTime)
    print "----------------------"

    #end of PrintInfo()

def ReadEncoder():
    DegreesPerPulse = (100.0/360.0) # 100 pulses in 360 degrees. Need to get floating numbers


    oldPinA = GPIO.input(21)

    ForwardCount = 0

    RequiredForwardCount = math.ceil(ForwardDegrees*DegreesPerPulse) #rounding up

    while True:

        encoderPinA = GPIO.input(21)
        encoderPinB = GPIO.input(20)

        if (encoderPinA == True) and (oldPinA == False):

            if encoderPinB == False:
                ForwardCount +=1
                print "Forward Count " + str(ForwardCount)



        oldPinA = encoderPinA

        if ForwardCount >=RequiredForwardCount:
            print "reached target"
            break
        #End of ReadEncoder
        
def TurnLightOn():
    GPIO.output(18, GPIO.HIGH)#turns on yellow signal LED

    #end of TurnLightOn()

def TurnLightOff():
    GPIO.output(18, GPIO.LOW)#turns off yellow signal LED

    #end of TurnLightOff()

def GetUserResponse():

    while True:

        #strings containing variety of possible responses for yes and no
        global yes
        global no
        yes = ["YES", "yes", "y", "Y", "Ye", "ye"]
        no = ["No", "NO", "no", "N"]

        #make AskUser response accessible globally
        global UserResponse

        try:
            print "-----------------------------"
            UserResponse = raw_input("Do you want to start from the beginning again? Enter Y or N: ")
            UserResponse = UserResponse.upper()#Make answer upper case
            if UserResponse in yes:
                UserResponse == "y"
                print "You wish to start again"
                break
            
            elif UserResponse in no:
                UserResponse == "N"
                print "You wish to exit"
                break
            else:
                sleep(0.2)
                print "Please respond yes or no"
                sleep(0.3)

        except:
           print "Please respond yes or no" 

    #end of GetUserResponse
            

"______________________________________"

#program structure

Initialise()

FlashSignalLight()

UserResponse = "y"

while UserResponse in ["YES", "yes", "y", "Y", "Ye", "ye"]:

    ReloadSettings() #show user what last settings are.

    GetUserInput()#Ask if user wants to reload these settings or enter new ones

    if AskUser in yes:
        ReloadSettings()
        
    if AskUser in no:
        LoadNewSettings()

    cycleCount = 1

    sleep(1)


    print "----------------------------------"

    UserResponse = raw_input("Please press s and enter to start: ")


    while cycleCount <= Cycles: #Each cycle takes at least 3.5 seconds

        print "Cycle Number: " +str(cycleCount)+" commencing"
        sleep(0.5)
        print "--------------------------------------------"

        
        MoveMotorForward()
        print "Motor Forwards"
        ReadEncoder()
        SwitchOffMotor()

        cycleCount +=1

        print "Waiting " + str(SleepTime)+" seconds before moving motor "
        print "---------------------------"
        sleep(SleepTime)
        

    PrintInfo () # things like cycle count and settings

    TurnLightOn()

    GetUserResponse()

    if UserResponse in yes:
        TurnLightOff()
        sleep(1)
        print "Starting again"
        sleep(1)

TurnLightOff()
GPIO.cleanup()
sleep(1)
print "Exiting...."
sleep(1)
exit    


