import smbus

class readFailure(Exception):
  pass

class i2cio:
  def __init__(self, address):
    self.bus = smbus.SMBus(1)
    target_address = 0x08
  
  def readData(self):
    try:
      data = self.bus.read_byte(address)
    except:
      raise readFailure
    return data
