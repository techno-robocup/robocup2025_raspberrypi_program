import smbus #Python 3
import time
import i2cio.i2cio import i2cio

if __name__ == "__main__":
    i2c = i2cio(0x08)

while True:
    message = input("Input message: ")
    i2cwriteData(message)
    data = i2c.readData()
    print(data)
    time.sleep(1)
