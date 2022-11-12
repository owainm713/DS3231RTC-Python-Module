#!/usr/bin/env python3
"""DS3231RTCexample, example file to use the DS3231 RTC (real time
clock) python module

created Novmember 12, 2022
last modified Novmember 12, 2022"""

"""
Copyright 2022 Owain Martin

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import DS3231RTC

myClock = DS3231RTC.DS3231(0x68)  # 0x68 is the i2c address

setupClock = False

if setupClock == True:
    myClock.set_control(EOSC = 0, A1IE = 1)
    myClock.set_clock(5,37,0, clockFormat = '12', amPM = 'PM')
    myClock.set_date(22,11, 8, 3)
    myClock.set_alarm1(4,15,0, clockFormat = '12', amPM = 'PM', alarmFreq = 'D')

currentTime = myClock.get_time()
if currentTime[3] != None:
    # 12hr format
    print(f"{currentTime[0]}:{currentTime[1]}:{currentTime[2]} {currentTime[3]}")
else:
    # 24hr format
    print(f"{currentTime[0]}:{currentTime[1]}:{currentTime[2]}")

d = myClock.get_date()
print(f"{d[0]}/{d[1]}/{d[2]} {d[4]}")

print(f"{myClock.get_temperature()}C")

flgs = myClock.get_status()
print(f"A1F:{flgs[0]}, A2F:{flgs[1]}, BSY:{flgs[2]}, OSF:{flgs[3]}")

myClock.clear_status()
