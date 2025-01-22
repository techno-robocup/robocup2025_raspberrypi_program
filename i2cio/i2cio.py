import smbus

class readFailure(Exception):
  pass

class writeFailure(Exception):
  pass

class i2cio:
  def __init__(self, address):
    self.bus = smbus.SMBus(1)
    target_address = 0x08

  def writeData(self,data):
    byte_data = [ord(c) for c in data]
    cmd = [0x00]
    try:
      self.bus.write_i2c_block_data(ADDRESS,cmd,byte_data)
    except:
      raise writeFailure

  def readData(self):
    try:
      data = self.bus.read_byte(address)
      recived_message = ''.join(chr(b)for b in data if b != 0)
    except:
      raise readFailure
    return data
