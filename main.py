import time
import random
from i2cio.i2cio import i2cio

if __name__ == "__main__":
    i2c_device = i2cio(0x08)
    while True:
        # Wait while next available
        while True:
            data = i2c_device.readData()
            if data is None:
                continue
            if data == 0x01:
                break
        a = list(map(int, input("Input two num: ").split()))
        i2c_device.writeData(a)
        while True:
            data = i2c_device.readData()
            if data is None:
                continue
            if data == 0x00:
                continue
            break
