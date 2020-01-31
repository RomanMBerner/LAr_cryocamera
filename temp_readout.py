# //////////////////////////////////////////////// //
#                                                  //
# python script to read the PT100 temperature      //
# sensor on the chip of the cryocamera.            //
# This script only reads the temperature on the    //
# camera chip but does not regulate the heating.   //
#                                                  //
# NOTE: NEVER USE THE CAMERA AT ROOM TEMPERATURE   //
# BUT ONLY AT CRYOGENIC TEMPERATURES.              //
#                                                  //
# Last modifications: 19.01.2019 by R.Berner       //
#                                                  //
# //////////////////////////////////////////////// //


#!/usr/bin/python
import time, math
import subprocess

if __name__ == "__main__":

	import max31865

	cs0Pin  = 5
	misoPin = 9
	mosiPin = 10
	clkPin  = 11
        heatPin = 26

	sens = max31865.max31865_heater(cs0Pin,misoPin,mosiPin,clkPin,heatPin,0)

        tempC = sens.readTemp()

        # First few measurements could be incorrect
        for i in range (0,10):
            sens.readTemp()
            time.sleep(0.2)

        tempC = sens.readTemp()

        while 1:
            time.sleep(1.)
            tempC = sens.readTemp()
            print "Current temperature: %.2f" % tempC

	GPIO.cleanup()
