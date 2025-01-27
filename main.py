import time
from i2cio.i2cio     import i2cio

if __name__ == "__main__":
    i2c_device = i2cio(0x08)

    while True:
        message = input("Input message: ")

        send_data = list(message.split())
        send_data = [ int(i) for i in send_data ]
        i2c_device.writeData(send_data)

        data = i2c_device.readData()
        print(f"Recived data: {data}")

        returnbits(data)
