'''
   beaglebone tank motor control

   copyright Kouji Yatou <kouji.yatou@gmail.com>

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

'''

import time
import beaglebone

class BeagleBoneTankDriver:
    """ BeagleBone tank driver class."""

    def __init__(self):
        beaglebone.exportAllGPIO() #export all gpio pins
        #PIN assign
        #left motoro driver and right motor driver.
        ML_IN1=70 #GPIO2_6
        ML_IN2=71 #GPIO2_7
        MR_IN1=72 #GPIO2_8
        MR_IN2=73 #GPIO2_9 
        self._all_pins=(ML_IN1,ML_IN2,MR_IN1,MR_IN2)
        self._left_motor=(ML_IN1,ML_IN2)
        self._right_motor=(MR_IN1,MR_IN2)
        
        #init GPIO mode
        for pin in self._all_pins:
            beaglebone.setGPIOWriteMode(pin)

    def __del__(self):
        #destructor.
        beaglebone.unexportAllGPIO()


 
    def stop(self):
        for pin in self._all_pins:
            beaglebone.gpioOff(pin)
   
    def goForward(self):
        self.__forwardMotor(self._left_motor)
        self.__forwardMotor(self._right_motor)
 
    def back(self):
        self.__backMotor(self._left_motor)
        self.__backMotor(self._right_motor)

    def turnLeft(self):
        self.__forwardMotor(self._left_motor)
        self.__backMotor(self._right_motor)

    def turnRight(self):
        self.__backMotor(self._left_motor)
        self.__forwardMotor(self._right_motor)

    def __forwardMotor(self,motor):
        """set forward motor."""
        beaglebone.gpioOn(motor[0])
        beaglebone.gpioOff(motor[1])

    def __backMotor(self,motor):
        """set back  motor."""
        beaglebone.gpioOff(motor[0])
        beaglebone.gpioOn(motor[1])

if __name__=='__main__':
    #test code
    tank=BeagleBoneTankDriver()
   
    tank.goforward()
    print 'GO! GO! GO!'
    time.sleep(2)
    tank.back()
    print 'oops! run away!!'
    time.sleep(3)
    
    print 'Ok,stop the tank.' 
    tank.stop()
    time.sleep(1)
