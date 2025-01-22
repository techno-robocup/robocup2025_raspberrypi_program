import smbus
import time

class readFailure(Exception):
  pass

class writeFailure(Exception):
  pass

class i2cio:
  def __init__(self, address):
    self.bus = smbus.SMBus(1)
    self.target_address = address

  def writeData(self, data:list[int]):
    cmd = 0x00
    #(address(int), cmd(int), data(list[int]))
    self.bus.write_i2c_block_data(self.target_address,cmd,data)

  def readData(self):
    data = self.bus.read_byte(self.target_address)
    recived_message = ''.join(chr(b)for b in data if b != 0)
    return data
