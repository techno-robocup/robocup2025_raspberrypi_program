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
    try:
      self.bus.write_i2c_block_data(self.target_address,cmd,data)
    except Exception as e:
      print("failed", e)

  def readData(self):
    data = 0x00
    try:
      data = self.bus.read_byte(self.target_address)
    except Exception as e:
      print("failed", e)
      return None
    return data
