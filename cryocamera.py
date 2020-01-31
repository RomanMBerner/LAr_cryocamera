# //////////////////////////////////////////////// //
#                                                  //
# python2 script to read the PT100 temperature     //
# sensor on the chip of the cryocamera.            //
# This script allows for setting a lower and an    //
# upper temperature, which will be set using a     //
# resistor chain within the camera case.           //
#                                                  //
# NOTE: NEVER USE THE CAMERA AT ROOM TEMPERATURE   //
# BUT ONLY AT CRYOGENIC TEMPERATURES.              //
#                                                  //
# Last modifications: 25.02.2019 by R.Berner       //
#                                                  //
# //////////////////////////////////////////////// //


#!/usr/bin/python
import math
import os
import subprocess
import time

if __name__ == "__main__":

    import max31865

    cs0Pin  = 5
    misoPin = 9
    mosiPin = 10
    clkPin  = 11
    heatPin = 26

    heat	= 0
    motion	= 0

    sens = max31865.max31865_heater(cs0Pin,misoPin,mosiPin,clkPin,heatPin,0)

    sens.heatOff()
    heat = 0

    # Define temperature range to operate the camera
    min_temp = -20.
    max_temp = -10.
    print "min_temp: %.2f C" % min_temp
    print "max_temp: %.2f C" % max_temp

    # Define temperature range to operate the motion
    motion_start = -70.
    motion_stop  =  45.

    # First few temp. measurements could be incorrect
    for i in range(10):
        time.sleep(0.2)
        sens.readTemp()

    try:

        while 1:

            time.sleep(1.)
            tempC = sens.readTemp()

            if tempC < min_temp and not heat:
                sens.heatOn()
                heat = 1
                print "Heating ON"

            if tempC > max_temp and heat:
                sens.heatOff()
                heat = 0
                print "Heating OFF"

            if tempC > motion_start and tempC < (motion_stop-10.) and not motion:
                process = subprocess.Popen(["sudo", "motion", "start"])
                motion = 1
                print "Motion START"

            if (tempC < motion_start or tempC > motion_stop) and motion:
                os.system("sudo service motion restart &> /dev/null &")
                os.system("sudo service motion stop &> /dev/null &")
                motion = 0
                print "Motion STOP"

            print "Current temperature: %.2f" % tempC
            try:
                os.system("scp /tmp/motion/cryostat/*snapshot.jpg lhep@130.92.139.15:/home/lhep/Desktop/cryostat/")
                os.system("sudo rm /tmp/motion/cryostat/*snapshot.jpg &> /dev/null")
            except:
                pass

    except KeyboardInterrupt:

        if heat:
            sens.heatOff()

        if motion:
            os.system("sudo service motion stop &> /dev/null &")

    GPIO.cleanup()
