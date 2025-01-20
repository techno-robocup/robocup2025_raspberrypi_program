from machine import I2C, Pin
import time

I2C_SLAVE_ADDRESS = 0x08

i2c = I2C(0, scl=Pin(22), sda=Pin(21))  #pin nom

recive_data = bytearray(32)
write_data = bytearray(32)

while True:
    try:
        i2c.readfrom(I2C_SLAVE_ADDRESS, recive_data)
        message = recive_data.decode('utf-8')
        print(message)
    except:
        print("Error cannot read data")
    time.sleep(1)
