"""
This library is an I2C API for pyboard.
Pre-Alpha v0.3 - Hyun Jun (Cryptos) An

Github : https://github.com/cryptosan/micropython-frostapi
"""
from pyb import I2C


class FrostAPI():
    """Initialize I2C bus to communicate with a device.

    1 is on X9(SCL), X10(SDA)
    2 is on Y9(SCL), Y10(SDA)

    :param bus: I2C bus, 1 or 2
    """
    def __init__(self, bus=1):
        self.i2c = I2C(bus)
        self._addr = None
        self.set_timeout()
        self.set_addr_size()

    def begin(self, mode, addr=0x12, baudrate=400000, gencall=False):
        """Initialize a device to communicate.

        :param mode: A mode of device, MASTER, or SLAVE.
        :param addr: An address for SLAVE.
        :param baudrate: SCL clock rate.
        :param gencall: If it supports general call mode.
        """
        self.i2c.init(mode=mode, addr=addr, baudrate=baudrate, gencall=gencall)

    def close(self):
        """Close the connection for communication."""
        if not self.is_init():
            self.not_init_device()
        self.i2c.deinit()

    def is_ready(self, addr):
        """Check the address of slave device.

        :param addr: An address of slave device.
        :return bool: Return True, if the address is connected to slave device.
        """
        return self.i2c.is_ready(addr)

    def is_init(self):
        """Check the init of device.

        :return bool: Return True, if the device is initiated.
        """
        return len(str(self.i2c).split(',')) > 1

    def is_master_mode(self):
        """Check the mode of device to use MASTER mode routines.

        :return bool: Return True, if the mode is `Master`.
        """
        if not self.is_init():
            self.not_init_device()
        return 'MASTER' in str(self.i2c)

    def scan_addr(self):
        """Scan all address of devices, which are connected.

        :return list: A list of addresses.
        """
        return self.i2c.scan()

    def set_addr(self, addr):
        self._addr = addr

    def get_addr(self):
        return self._addr

    def set_timeout(self, timeout=5000):
        """Set timeout in miliseconds to wait for write."""
        self._timeout = timeout

    def get_timeout(self):
        """Get timeout in miliseconds."""
        return self._timeout

    def set_addr_size(self, addr_size=8):
        """Set width of `memaddr`.

        :param addr_size: 8 or 16 bit. (default is 8 bit.)
        """
        self._addr_size = addr_size

    def get_addr_size(self):
        """Get width of `memaddr`.

        :return int: A 8 or 16 bit value of width of `memaddr`.
        """
        return self._addr_size

    def send_to(self, buf, addr):
        """Send a data to slave device safely with checking address routine."""
        if not self.is_ready(addr):
            self.not_found_address()
        self._send(buf=buf, addr=addr, timeout=self.get_timeout())

    def _send(self, buf, addr=0x00, timeout=5000):
        """Send a data to slave device unsafely without checking address
        routine.

        :param buf: A data to send (Can be an integer, or a buffer)
        :param addr: An address of slave device to send a data.
        :param timeout: A miliseconds to wait to send.
        """
        self.i2c.send(send=buf, addr=addr, timeout=timeout)

    def recv_from(self, size, addr):
        """Receive a data from slave device safely with checking address
        routine.

        :return bytes: A buffer of the bytes received.
        """
        if not self.is_ready(addr):
            self.not_found_address()
        return self._recv(size=size, addr=addr, timeout=self.get_timeout())

    def _recv(self, size, addr=0x00, timeout=5000):
        """Receive a data from slave device unsafely without checking address
        routine.

        :param size: An integer, which is the number of bytes to receive,
                     or buffer, which will be filled with received bytes.
        :param addr: An address of slave device to receive a data.
        :return bytes: A buffer of the bytes received.
        """
        if not self.is_ready(addr):
            self.not_found_address()
        return self.i2c.recv(recv=size, addr=addr, timeout=timeout)

    def write_mem(self, buf, memaddr):
        """Access to memory safely with a routine of checking I2C object init.
        Can be used in only `Master` mode.

        :param buf: A data (or buffer) to write to memory.
        :param memaddr: An address of memory
        """
        if not self.is_master_mode():
            self.not_init_by_master_mode()
        self._write(buf=buf, addr=self.get_addr(), memaddr=memaddr)

    def _write(self, buf, addr, memaddr):
        """Access to memory unsafely, control `mem_write()` without a routine
        of checking I2C object init.
        Can be used in only `Master` mode.

        :param buf: A data (or buffer) to write to memory.
        :param addr: An address of device what you want to communicate.
        :param memaddr: An address of memory where you want to write.
        """
        self.i2c.mem_write(data=buf,
                           addr=addr,
                           memaddr=memaddr,
                           timeout=self.get_timeout(),
                           addr_size=self.get_addr_size())

    def read_mem(self, size, memaddr):
        """Access to memory safely with a routine of checking I2C object init.
        Can be used in only `Master` mode.

        :param size: An integer(number of bytes) to read, or a buffer to read.
        :param memaddr: An address of memory where you want to read.
        :return bytes: Read a number of bytes as much as `size`.
        """
        if not self.is_master_mode():
            self.not_init_by_master_mode()
        return self._read(size=size, addr=self.get_addr(), memaddr=memaddr)

    def _read(self, size, addr, memaddr):
        """Access to memory unsafely, control `mem_read()` without a routine
        of checking I2C object init.
        Can be used in only `Master` mode.

        :param size: An integer(number of bytes) to read, or a buffer to read.
        :param addr: An address of device what you want to communicate.
        :param memaddr: An address of memory where you want to read.
        :return bytes: Read a number of bytes as much as `size`.
        """
        return self.i2c.mem_read(data=size,
                                 addr=addr,
                                 memaddr=memaddr,
                                 timeout=self.get_timeout(),
                                 addr_size=self.get_addr_size())

    def not_found_address(self):
        """An exception when doesn't init address of device."""
        raise Exception("Couldn't find the device address!")

    def not_init_device(self):
        """An exception when doesn't init device."""
        raise Exception("Didn't init your device yet!")

    def not_init_by_master_mode(self):
        """An exception when doesn't init by Master mode."""
        raise Exception("Didn't init your device by Master mode.")
