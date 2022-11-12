# DS3231RTC-Python-Module

Python 3.x to use with the DS3231 RTC (Real Time Clock). Testing done with a DS3231 breakout
 board from Adafuit and a Raspberry Pi3.

created Nov 8, 2022
modified NOv 8, 2022

This uses i2C and requires the smbus python library.

Connections to the DS3231 board from the Pi are as follows:
- Pi 3.3V to DS3231 Vin
- Pi Gnd to DS3231 Gnd
- Pi SCL to DS3231 SCL
- Pi SDA to DS3231 SDI
- DS3231 Bat - not connected
- DS3231 32K - not connected
- Pi GPIO # to DS3231 SQW(INT pin) - optional, requires a pullup resistor
- DS3231 RST - not connected

The DS3231 datasheet is useful for figuring out how to correctly configure the DS3231 for your application.

Current functions include:
- set_control(EOSC = 0, A1IE = 0, A2IE = 0, INTCN = 1, BBSQW = 0, RS1 = 1, RS2 = 1, EN32K = 0) - sets various control functions
- set_clock(hours, minutes = 0, seconds = 0, clockFormat = '12', amPM = 'AM') - function to set the clocks times
- set_date(year, month, day, dow = None) - function to set the clocks date.
- set_dow(dow) - function to set the day of the week (dow)
- set_alarm1(hours, minutes = 0, seconds = 0, clockFormat = '12', amPM = 'AM', day = 0, dayFormat = 'Date', alarmFreq = 'D') - function to set alarm1
- set_alarm2(hours, minutes = 0, clockFormat = '12', amPM = 'AM', day = 0, dayFormat = 'Date', alarmFreq = 'D') - function to set alarm2
- change_clock_format(clockFormat = '12') -function to change the clock format ('12' or '24' hr) without having to reset the clock's time
- get_time() - returns a tuple with the time in format (hours, minutes, seconds, amPM) 
- get_date() - returns a tuple with the date in format (dayInMonth, month, year, centuryFlag, dow)
- get_status() - return a tuple with various status flags in format (A1F, A2F, BSY, OSF)
- get_temperature() - returns the temperature, in Celcius, from the onboard temperature sensor
- clear_status() - function to clear the status flags in the status register (0x0F)

Notes for the set_alarm functions
dayFormat can be either 'Date' or 'Day' which determines if the alarm will trigger on a dow or date when alarmFreq is set to 'C'
Valid alarmFreq values are
- 'S' - once per second (alarm1 only)
- 'M' - every minute (when sec match)
- 'H' - every hour (when min/sec match)
- 'D' - daily (when hr/min/sec match)   
- 'C' - every week/month (when DOW/Date and hr/min/sec match)