#!/usr/bin/env python3
"""DS3231RTC, python module for the DS3231 RTC (real time
clock)

created October 22, 2022
last modified October 25, 2022"""

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

import smbus

class DS3231:

    def __init__(self, i2cAddress):

        self.i2cAddress = i2cAddress
        self.bus = smbus.SMBus(1)

        return

    def multi_access_write_i2c(self, reg=0x00, regValues = [0x00]):
        """multi_access_write_i2c, function to write to multiple registers at
        once"""
        
        self.bus.write_i2c_block_data(self.i2cAddress, reg, regValues)

        return
    
    def single_access_write(self, reg=0x00, regValue = 0):
        """single_access_write, function to write to a single 8 bit
        data register"""                  
       
        self.bus.write_byte_data(self.i2cAddress,reg, regValue)
        
        return

    def multi_access_read_i2c(self, reg=0x00, numRead = 1):
        """multi_access_read_i2c, function to read multiple registers at
        once"""

        dataTransfer = self.bus.read_i2c_block_data(self.i2cAddress, reg, numRead)

        return dataTransfer

    def single_access_read(self, reg=0x00):
        """single_access_read, function to read a single 8 bit data
        register"""                  
       
        dataTransfer=self.bus.read_byte_data(self.i2cAddress,reg)
        
        return dataTransfer

    def twos_complement_conversion(self,tempData):
        """twos_complement_conversion, function to change the 10 bit
        temperature value split across 2 bytes, with 2 decimal bits
        from 2s complement to normal binary/decimal"""

        signBit= (tempData & 0x200)>>9
        tempData = tempData & 0x1FF  # strip off sign bit        

        if signBit == 1:  # negative number        
            x = tempData
            x = x^0x3FF
            x = -(x + 1)
        else: # positive number        
            x = tempData

        temperature = x/pow(2,2)

        return temperature

    def get_temperature(self):
        """get_temperature, function to return the temperature
        stored in registers 0x11 and 0x12"""
    
        tempBytes = self.multi_access_read_i2c(0x11, 2)
        tempData = (tempBytes[0]<<2)+ (tempBytes[1]>>6)
        temperature = self.twos_complement_conversion(tempData)
        
        return temperature

    
    def set_control(self, EOSC = 0, A1IE = 0, A2IE = 0, INTCN = 1, BBSQW = 0, RS1 = 1, RS2 = 1, EN32K = 0):
        """set_control, function to set various control features of the DS3231 RTC. This
        sets registers 0x0E (Control) and 0x0F (Status). This will clear the status flags in
        in the Status register"""
        
        controlRegValue = (EOSC<<7) + (BBSQW<<6) + (RS2<<4) + (RS1<<3) + (INTCN<<2) + (A2IE<<1) + A1IE
        statusRegValue = EN32K<<3
        
        self.multi_access_write_i2c(0x0E, regValues = [controlRegValue, statusRegValue])
        
        return

    def set_dow(self, dow):
        """set_dow, function to set the day of the week from
        1-7 in register 0x03"""
        
        self.single_access_write(reg=0x3, regValue = dow)
        
        return

    def set_date(self, year, month, day, dow = None):
        """set_date, function to set the date. Registers 0x3-0x6"""
        
        if dow != None:
            self.set_dow(dow)
            
        dayRegValue = ((day//10)<<4) + (day%10)
        monthRegValue = ((month//10)<<4) + (month%10)
        yearRegValue = ((year//10)<<4) + (year%10)
        
        self.multi_access_write_i2c(0x04, regValues = [dayRegValue, monthRegValue, yearRegValue])
            
        return

    def set_clock(self, hours, minutes = 0, seconds = 0, clockFormat = '12', amPM = 'AM'):
        """set_clock, function to set the time registers 0x00 to 0x02.
        Values are stored in binary coded decimal (BCD)"""
        
        secRegValue = ((seconds//10)<<4) + (seconds%10) # convert to BCD
        minRegValue = ((minutes//10)<<4) + (minutes%10) # convert to BCD
        
        if clockFormat == '12':
            clockFormatBit = 0b1
            
            if amPM == 'PM':
                amPMBit = 0b1
            else:
                amPMBit = 0b0
                
            hrRegValue = ((hours//10)<<4) + (hours%10) # convert to BCD
            hrRegValue = (clockFormatBit<<6) +(amPMBit<<5) + hrRegValue
                
        else:
            clockFormatBit = 0b0
            hrRegValue = (clockFormatBit<<6) + ((hours//10)<<4) + (hours%10)
            
        self.multi_access_write_i2c(0x00, regValues = [secRegValue, minRegValue, hrRegValue])
            
        return

    def set_alarm1(self, hours, minutes = 0, seconds = 0, clockFormat = '12', amPM = 'AM', day = 0, dayFormat = 'Date', alarmFreq = 'D'):
        """set_alarm1, function to set the alarm1 registers 0x07 to 0x0A"""
        
        secRegValue = ((seconds//10)<<4) + (seconds%10) # convert to BCD
        minRegValue = ((minutes//10)<<4) + (minutes%10) # convert to BCD
        
        if clockFormat == '12':
            clockFormatBit = 0b1
            
            if amPM == 'PM':
                amPMBit = 0b1
            else:
                amPMBit = 0b0
                
            hrRegValue = ((hours//10)<<4) + (hours%10) # convert to BCD
            hrRegValue = (clockFormatBit<<6) +(amPMBit<<5) + hrRegValue
                
        else:
            clockFormatBit = 0b0
            hrRegValue = (clockFormatBit<<6) + ((hours//10)<<4) + (hours%10)
               
        if dayFormat == 'Date':
            dayBit = 0b0
        else:
            dayBit = 0b1        
           
        dayRegValue = (dayBit<<6) + ((day//10)<<4) + (day%10)
        
        # add alarm mask bits, valid alarmFreq values:
        # 'S' - once per second, 'M' - every minute (when sec match)
        # 'H' - every hour (when min/sec match), 'D' - daily (when hr/min/sec match)   
        # 'C' - every week/month (when DOW/Date and hr/min/sec match)
            
        alarm1Masks = {'S':[1,1,1,1],
                       'M':[0,1,1,1],
                       'H':[0,0,1,1],
                       'D':[0,0,0,1],
                       'C':[0,0,0,0]}
        
        alarmMask = alarm1Masks.get(alarmFreq, [0,0,0,1])
        
        secRegValue = (alarmMask[0]<<7) + secRegValue
        minRegValue = (alarmMask[1]<<7) + minRegValue
        hrRegValue = (alarmMask[2]<<7) + hrRegValue
        dayRegValue = (alarmMask[3]<<7) + dayRegValue    
            
        self.multi_access_write_i2c(0x07, regValues = [secRegValue, minRegValue, hrRegValue, dayRegValue])
            
        return

    def set_alarm2(self, hours, minutes = 0, clockFormat = '12', amPM = 'AM', day = 0, dayFormat = 'Date', alarmFreq = 'D'):
        """set_alarm2, function to set the alarm2 registers 0x0B to 0x0D"""
        
        minRegValue = ((minutes//10)<<4) + (minutes%10) # convert to BCD
        
        if clockFormat == '12':
            clockFormatBit = 0b1
            
            if amPM == 'PM':
                amPMBit = 0b1
            else:
                amPMBit = 0b0
                
            hrRegValue = ((hours//10)<<4) + (hours%10) # convert to BCD
            hrRegValue = (clockFormatBit<<6) +(amPMBit<<5) + hrRegValue
                
        else:
            clockFormatBit = 0b0
            hrRegValue = (clockFormatBit<<6) + ((hours//10)<<4) + (hours%10)
               
        if dayFormat == 'Date':
            dayBit = 0b0
        else:
            dayBit = 0b1        
           
        dayRegValue = (dayBit<<6) + ((day//10)<<4) + (day%10)
        
        # add alarm mask bits, valid alarmFreq values:
        # 'M' - once per minute (at 00 sec)
        # 'H' - every hour (when min match), 'D' - daily (when hr/min match)
        # 'C' - every week/month (when DOW/Date and hr/min match)
        
        alarm2Masks = {'M':[1,1,1],
                       'H':[0,1,1],
                       'D':[0,0,1],
                       'C':[0,0,0]}
        
        alarmMask = alarm2Masks.get(alarmFreq, [0,0,1])    
        
        minRegValue = (alarmMask[0]<<7) + minRegValue
        hrRegValue = (alarmMask[1]<<7) + hrRegValue
        dayRegValue = (alarmMask[2]<<7) + dayRegValue    
            
        self.multi_access_write_i2c(0x0B, regValues = [minRegValue, hrRegValue, dayRegValue])
            
        return
    
    def change_clock_format(self, clockFormat = '12'):
        """change_clock_format, function to change the clock format between
        12hr and 24hr formats. This changes the hour register 0x02."""       
        
        if clockFormat == '12':
            clockFormatBit = 0b1
        else:
            clockFormatBit = 0b0        
        
        if clockFormatBit == 0b0:
            # 24hr format
            # check current format
            # if 12hr get hour value and if PM add 12 to it
            cTime = self.get_time()
            if cTime[3] == 'PM':
                hour = cTime[0] + 12
            else:
                hour = cTime[0]
                
            regValue = ((hour//10)<<4) + (hour%10) # convert to BCD
        else:
            # 12hr format
            # check current format
            # if 24hr get hour and if >12 minus 12 and set PM
            cTime = self.get_time()
            if cTime[0] > 12:
                hour = cTime[0] - 12
                amPM = 'PM'
            else:
                hour = cTime[0]
                amPM = cTime[3]
            
            if amPM == 'PM':
                amPMBit = 0b1
            else:
                amPMBit = 0b0
                
            regValue = (amPMBit<<5) + ((hour//10)<<4) + (hour%10)    
        
        regValue =  (clockFormatBit<<6) + regValue    
        self.single_access_write_i2c(reg=0x2, regValue = regValue)

        return

    def get_time(self):
        """get_time, function to return the time stored in the time
        registers 0x00 to 0x02. Data is stored in binary coded deciaml (BCD)"""

        timeBytes = self.multi_access_read_i2c(0x00, 3)

        seconds = ((timeBytes[0] & 0x70)>>4)*10 + (timeBytes[0] & 0x0F)
        minutes = ((timeBytes[1] & 0x70)>>4)*10 + (timeBytes[1] & 0x0F)
        hourFlag = (timeBytes[2] & 0x40)>>6

        if hourFlag == 1:
            # 12hr mode
            if (timeBytes[2] & 0x20)>>5 == 1:
                amPM = 'PM'
            else:
                amPM = 'AM'
            
            hours = ((timeBytes[2] & 0x10)>>4)*10 + (timeBytes[2] & 0x0F)            
        else:
            # 24hr mode         
            hours = ((timeBytes[2] & 0x30)>>4)*10 + (timeBytes[2] & 0x0F)
            amPM = None       
            
        return (hours, minutes, seconds, amPM)

    def get_date(self):
        """get_date, function to return the date information stored in
        the date registers 0x03 to 0x06. Data is stored in binary coded
        deciaml (BCD)"""
    
        dateBytes = self.multi_access_read_i2c(0x3, 4)
        
        dow = dateBytes[0]
        dayInMonth = ((dateBytes[1] & 0x30)>>4)*10 + (dateBytes[1] & 0x0F)
        month = ((dateBytes[2] & 0x10)>>4)*10 + (dateBytes[2] & 0x0F)
        centuryFlag = ((dateBytes[2] & 0x80)>>7)
        year = ((dateBytes[3] & 0xF0)>>4)*10 + (dateBytes[3] & 0x0F)        
        
        return (dayInMonth, month, year, centuryFlag, dow)


    def get_status(self):
        """get_status, function to read the status register 0x0F and return the
        OSF, BSY, A1F and A2F flags"""
        
        statusRegValue = self.single_access_read(reg=0x0F)
        
        OSF = (statusRegValue & 0x80)>>7
        BSY = (statusRegValue & 0x04)>>2
        A2F = (statusRegValue & 0x02)>>1
        A1F = (statusRegValue & 0x01)
        
        return (A1F, A2F, BSY, OSF)

    def clear_status(self):
        """clear_status, function to clear the flags in the
        status register 0x0F"""
        
        self.single_access_write(reg=0x0F, regValue = 0x00)
        
        return

if __name__ == "__main__":

    myClock = DS3231(0x68)

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
    

    
