"""
This library is an I2C API for pyboard.
Pre-Alpha v0.2 - Hyun Jun (Cryptos) An

Github : https://github.com/cryptosan/micropython-frostapi
"""
from pyb import I2C


class FrostAPI():
    _ADDR = 0x00

    def __init__(self, bus=1):
        self.i2c = I2C(bus)

    def begin(self, mode=I2C.MASTER, addr=0x12, baudrate=400000,
              gencall=False):
        self._ADDR = addr
        self.i2c.init(mode=mode, addr=self._ADDR, baudrate=baudrate,
                      gencall=gencall)

    def close(self):
        if self.is_init() is False:
            self.not_init_device()
        self.i2c.deinit()

    def is_ready(self):
        return self.i2c.is_ready(self.get_addr())

    def is_init(self):
        return len(str(self.i2c).split(',')) > 1

    def scan_addr(self):
        return self.i2c.scan()

    def set_addr(self, addr):
        self._ADDR = addr

    def get_addr(self):
        return self._ADDR

    def _send(self, buf, addr=0x00, timeout=5000):
        if self.is_ready() is False:
            self.not_found_address()
        self.i2c.send(send=buf, addr=addr, timeout=timeout)

    def _recv(self, size, addr=0x00, timeout=5000):
        if self.is_ready() is False:
            self.not_found_address()
        return self.i2c.recv(recv=size, addr=addr, timeout=timeout)

    def _write(self, buf, addr, memaddr, timeout=5000, addr_size=8):
        if self.is_ready() is False:
            self.not_found_address()
        self.i2c.mem_write(data=buf,
                           addr=addr,
                           memaddr=memaddr,
                           timeout=timeout,
                           addr_size=addr_size)

    def _read(self, size, addr, memaddr, timeout=5000, addr_size=8):
        if self.is_ready() is False:
            self.not_found_address()
        return self.i2c.mem_read(data=size,
                                 addr=addr,
                                 memaddr=memaddr,
                                 timeout=timeout,
                                 addr_size=addr_size)

    def not_found_address(self):
        raise Exception("Couldn't find the device address!")

    def not_init_device(self):
        raise Exception("Didn't init your device yet!")
