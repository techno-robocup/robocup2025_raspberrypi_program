import smbus #Python 3
import time

bus = smbus.SMBus(1) #Pass

ADDRESS = 0x08

def writeData():
    #byte_data = [ord(c) for c in data]
    try:
        bus.write_i2c_block_data(ADDRESS,)
    except:
        print("Error cannot write data")
        return -1

def readData():
    try:
        data = bus.read_byte(ADDRESS)
        return data
    except:
        print("Error cannot read data")
        return -1

while True:
    writeData()
    data = readData()
    print(data)
    time.sleep(1)
