import smbus
import

bus = smbus.SMBus(1) #Pass

address = 0x08

def readData():
    try:
        data = bus.read_byte(address)
        return data
    except:
        return -1

while True:
    data = readData()
    time.sleep(1)
