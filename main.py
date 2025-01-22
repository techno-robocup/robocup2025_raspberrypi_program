import time
from i2cio.i2cio     import i2cio

if __name__ == "__main__":
    i2c_device = i2cio(0x08)  # I2Cアドレスを設定

    while True:
        message = input("Input message: ")

        try:
            send_data = lsit(message.split())
            send_data = [ int(i) for i in range(send_data) ]
            i2c_device.writeData(send_data)

        except Exception as e:
            print(f"Error: {e}")

        time.sleep(1)
