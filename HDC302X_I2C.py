import machine
from machine import Pin, SoftI2C
import time

HDC302X_ADDR = 0x44 

i2c = SoftI2C(
    scl=Pin(5),
    sda=Pin(4),
    freq=400_000
)

sdaPIN=machine.Pin(4)
sclPIN=machine.Pin(5)
i2c=machine.I2C(0,sda=sdaPIN, scl=sclPIN, freq=400000)

def scanI2C():
    devices = i2c.scan()
    if len(devices) != 0:
        print('Number of I2C devices found=',len(devices))
        for device in devices:
            print("Device Hexadecimel Address= ",hex(device))
    else:
        print("No device found")


def heaterOff():
    i2c.writeto(HDC302X_ADDR, b'\x30\x66') # make sure heater is off
    
def heaterOn():
    i2c.writeto(HDC302X_ADDR, b'\x30\x6D')  # Turn heater on

def setI2C(sclPIN, sdaPIN, freq):
    i2c = SoftI2C(scl=Pin(sclPIN), sda=Pin(sdaPIN), freq=(freq))

def setAddr(addr):
    HDC302X_ADDR = addr

def getMeasurement():

    i2c.writeto(HDC302X_ADDR, b'\x24\x00')
    time.sleep(0.015)
    i2c.writeto(HDC302X_ADDR, b'\xE0\x00') # reset measurement pointer
    
    raw_data = i2c.readfrom(HDC302X_ADDR, 6) # get 4 bytes

    # Reassemble temperature 
    temp_high = raw_data[0]
    temp_low  = raw_data[1]
    temp_raw  = (temp_high << 8) | temp_low

    # CRC for temperature
    temp_crc  = raw_data[2]

    # Reassemble humidity 
    hum_high  = raw_data[3]
    hum_low   = raw_data[4]
    hum_raw   = (hum_high << 8) | hum_low

    # CRC for humidity
    hum_crc   = raw_data[5]

    temperature_c = (temp_raw / 65536) * 165.0 - 40.0
    humidity_rh   = (hum_raw  / 65536) * 100.0
    measurement = (temperature_c, humidity_rh)
    print("Temp: {:.2f}C  Humidity: {:.2f}%".format(temperature_c, humidity_rh))
    
    return measurement 
    

