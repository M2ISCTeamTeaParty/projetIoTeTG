#!/usr/bin/python
#--------------------------------------
#    ___  ___  _ ____
#   / _ \/ _ \(_) __/__  __ __
#  / , _/ ___/ /\ \/ _ \/ // /
# /_/|_/_/  /_/___/ .__/\_, /
#                /_/   /___/
#
#  lcd_16x2.py
#  16x2 LCD Test Script
#
# Author : Matt Hawkins
# Date   : 06/04/2015
#
# http://www.raspberrypi-spy.co.uk/
#
# Copyright 2015 Matt Hawkins
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#--------------------------------------

# The wiring for the LCD is as follows:
# 1 : GND
# 2 : 5V
# 3 : Contrast (0-5V)*
# 4 : RS (Register Select)
# 5 : R/W (Read Write)       - GROUND THIS PIN
# 6 : Enable or Strobe
# 7 : Data Bit 0             - NOT USED
# 8 : Data Bit 1             - NOT USED
# 9 : Data Bit 2             - NOT USED
# 10: Data Bit 3             - NOT USED
# 11: Data Bit 4
# 12: Data Bit 5
# 13: Data Bit 6
# 14: Data Bit 7
# 15: LCD Backlight +5V**
# 16: LCD Backlight GND

#import
import time
import sense_utils
import datetime
import RPi.GPIO as GPIO
from sense_utils import *
from etg_mother import *
from battery import Battery
from raspberry import Config

init_bn_battery_to_charge = 0

#init
config = Config()
try:

    buttonOnOff = True
    ledState = False
    add_battery_button = True
    count = 0
    stateOnOff = False
    init = False
    end_init = False

    batA = Battery()
    batB = Battery()
    batC = Battery()

    batteries = []

    # Send some test
    print("Come on man, press the button!")
    config.lcd_string(time.ctime(), Config.LCD_LINE_1)

    while True:
        buttonOnOff = GPIO.input(Config.buttonPin)
        # ON
        if buttonOnOff == False and stateOnOff == False and end_init == False:
            #GPIO.output(Config.LEDPinRed, True)
            print("LED ON")
            config.lcd_string("Rasbperry Pi On", Config.LCD_LINE_1)
            config.lcd_string("choisir nb batterie", Config.LCD_LINE_2)

            #launch eTG
            authentication()

            cookies = getCookies()
            charging_time = []
            for cookie in cookies:
                subscribe(cookie)
                timeForCharge = getChargingTime(getCookieTemperature(cookie))
                print(timeForCharge)
                charging_time.append(timeForCharge)

                timeeforcharge_formathms = str(datetime.timedelta(seconds=((timeForCharge * 100) * 60)))
                print('il faudra ' + timeeforcharge_formathms + ' minutes pour charger le ' + cookie.label)
                end_init = True

            # get batteries
            batA = Battery(id=1, label=cookies[0].label, max=10, charging_time=charging_time[0])
            batB = Battery(id=2, label=cookies[1].label, max=10, charging_time=charging_time[1])
            batC = Battery(id=3, label=cookies[2].label, max=10, charging_time=charging_time[2])

            if not (batA == None) or (batB == None) or (batC == None):
                batteries = [batA, batB, batC]


            stateOnOff = True
            time.sleep(0.5)

        if buttonOnOff == False and stateOnOff == True and end_init == False:
            GPIO.output(Config.LEDPinRed, False)
            print("LED OFF")
            config.lcd_string("Rasbperry Pi OFF", Config.LCD_LINE_1)
            config.lcd_string("Au revoir (^_^)", Config.LCD_LINE_2)

            # for simulation fin utilisation battery - reset
            for bat in batteries:
                if bat.etat == 100:
                    bat.etat = 0

            stateOnOff = False
            init = False
            time.sleep(0.5)

        # si allume
        if stateOnOff == True:
            init = True
            # init
            add_battery_button = GPIO.input(Config.buttonPinCount)

            if add_battery_button == False:
                init_bn_battery_to_charge += 1
                if init_bn_battery_to_charge > 3:
                    init_bn_battery_to_charge = 1

                config.lcd_string("Nbr de chargeur", Config.LCD_LINE_1)
                config.lcd_string(str(init_bn_battery_to_charge), Config.LCD_LINE_2)
                print("Number OF led: ", init_bn_battery_to_charge)
                time.sleep(0.5)

            buttonOnOff = GPIO.input(Config.buttonPin)

            if buttonOnOff == False:
                end_init = True
           
            elif end_init == True:
                #end_init = False
                # launch charge
                if not (batteries == []):
                    batteries = [batA, batB, batC]
                    launch_charge(init_bn_battery_to_charge = init_bn_battery_to_charge, p_batteries=batteries)
                    if init_bn_battery_to_charge == 1:
                        GPIO.output(Config.LEDPinRed, True)
                        config.lcd_string("Battry Cum", Config.LCD_LINE_1)
                        config.lcd_string("100% (^_^)", Config.LCD_LINE_2)
                        
                    # for simulation fin utilisation battery - reset
                    init_bn_battery_to_charge = -1
                    for bat in batteries:
                        if bat.etat == 100:
                            bat.etat = 0
                            print(bat.id)

                    end_init = False
except KeyboardInterrupt:
    pass
finally:
    config.lcd_byte(0x01, Config.LCD_CMD)
    config.lcd_string("Goodbye!", Config.LCD_LINE_1)
    GPIO.cleanup()

