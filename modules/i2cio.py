import smbus
import time


class readFailure(Exception):
    pass


class writeFailure(Exception):
    pass


class i2cio:

    def __init__(self, address):
        """
        Initializes an I2C connection with the target device.

        Args:
            address (int): The address of the target device on the I2C bus.
        """
        self.bus = smbus.SMBus(1)
        self.target_address = address

    def writeData(self, data: list[int]):
        """
        Writes a list of data to the target device on the I2C bus.

        Args:
            data (list[int]): The list of data to write to the target device.

        Raises:
            Exception: When the write operation fails.
        """
        cmd = 0x00
        #(address(int), cmd(int), data(list[int]))
        try:
            self.bus.write_i2c_block_data(self.target_address, cmd, data)
        except Exception as e:
            print("failed", e)

    def readData(self):
        """
        Reads data from the target device on the I2C bus.

        Returns:
            int: The data read from the target device on the I2C bus.
            None: When the read operation fails.
        """
        data = 0x00
        try:
            data = self.bus.read_byte(self.target_address)
        except Exception as e:
            print("failed", e)
            return None
        return data
