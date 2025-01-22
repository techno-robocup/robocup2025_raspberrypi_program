import smbus #Python 3
import time

bus = smbus.SMBus(1) #Pass

ADDRESS = 0x08
def writeData():
    byte_data = [ord(c) for c in data]
    try:
        bus.write_i2c_block_data(ADDRESS, ,0x00,byte_data)
    except:
        print("Error cannot write data")
        return -1

def readData():
    try:
        data = bus.read_byte(ADDRESS,0x00,32)
        recived_message = ''.join(chr(b)for b in data if b != 0)
        return data
    except:
        print("Error cannot read data")
        return -1

while True:
    message = input("Input message: ")
    writeData(message)
    data = readData()
    print(data)
    time.sleep(1)
