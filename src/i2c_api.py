"""
	This library is an I2C API for micro-python.

	Pre-Alpha v0.1 - Yi Soo, An

	Github : https://github.com/yisoo/micropython-i2c_api
"""
from pyb import I2C

class Raises():
	@staticmethod
	def device_address():
		raise Exception("Couldn't find the device address!")


	@staticmethod
	def device_init():
		raise Exception("The device didn't init yet!")


class I2C_API():
	_ADDR = 0x00

	def __init__(self, bus=1):
		self.i2c = I2C(bus)


	def begin(self, mode=I2C.MASTER, addr=0x12, baudrate=400000, gencall=False):
		self.i2c.init(mode=mode, addr=addr, baudrate=baudrate, gencall=gencall)


	def close(self):
		if self.is_init():
			self.i2c.deinit()
		else:
			Raises.device_init()


	def is_ready(self):
		return self.i2c.is_ready(self.get_addr())


	def is_init(self):
		return len(str(self.i2c).split(',')) > 1


	def addr_scan(self):
		return self.i2c.scan()


	def set_addr(self, addr):
		self._ADDR = addr


	def get_addr(self):
		return self._ADDR


	def _send(self, buf, addr=0x00, timeout=5000):
		if self.is_ready():
			self.i2c.send(send=buf, addr=addr, timeout=timeout)
		else:
			Raises.device_address()


	def _recv(self, size, addr=0x00, timeout=5000):
		temp = None

		if self.is_ready():
			temp = self.i2c.recv(recv=size, addr=addr, timeout=timeout)
		else:
			Raises.device_address()

		return temp


	def _write(self, buf, addr, memaddr, timeout=5000, addr_size=8):
		if self.is_ready():
			self.i2c.mem_write(
					data=buf, 
					addr=addr, 
					memaddr=memaddr, 
					timeout=timeout, 
					addr_size=addr_size
					)
		else:
			Raises.device_address()


	def _read(self, size, addr, memaddr, timeout=5000, addr_size=8):
		temp = None

		if self.is_ready():
			temp = self.i2c.mem_read(
						data=size, 
						addr=addr, 
						memaddr=memaddr, 
						timeout=timeout, 
						addr_size=addr_size
						)
		else:
			Raises.device_address()

		return temp
