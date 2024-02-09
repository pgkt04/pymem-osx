import ctypes
from pymem import process
from sys import platform

class PyMem:
  def __init__(self, process_name: str) -> None:
    assert platform == "Darwin", "PyMem only supports MacOS (64-bit ARM)"
    self.process_name = process_name
    self.pid = process.get_pid_by_name(process_name)
    assert self.pid != -1, "Failed to find process"
    self.task = process.get_task(self.pid)

  def read_buffer(self, address: int, size: int) -> bytes:
    buffer = ctypes.create_string_buffer(size)
    bytes_read = process.read(self.task, address, buffer, size)
    assert bytes_read == size, f"Failed to read buffer, only read {bytes_read} bytes out of {size} bytes"
    return buffer.raw

  def read_int32(self, address: int) -> int: pass
  def read_int64(self, address: int) -> int: pass
  def read_float(self, address: int) -> float: pass
  def read_double(self, address: int) -> float: pass
  def read_bool(self, address: int) -> bool: pass
  def read_bytes(self, address: int, size: int) -> bytes: pass
  def write_buffer(self, address: int, buffer: bytes) -> None: pass
  def write_int32(self, address: int, value: int) -> None: pass
  def write_int64(self, address: int, value: int) -> None: pass
  def write_float(self, address: int, value: float) -> None: pass
  def write_double(self, address: int, value: float) -> None: pass
  def write_bool(self, address: int, value: bool) -> None: pass
  def get_modules(self, extended: bool = False) -> list: pass