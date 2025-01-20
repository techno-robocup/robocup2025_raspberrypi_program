import smbus #Python 3
import time

bus = smbus.SMBus(1) #Pass

address = 0x08

def writeData():
    try:
        data = [0x01, 0x02, 0x03, 0x04]
        bus.write_byte(address, data)
    except:
        return -1

def readData():
    try:
        data = bus.read_byte(address)
        return data
    except:
        return -1

while True:
    data = readData()
    print(data)
    time.sleep(1)
