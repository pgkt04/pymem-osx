import ctypes
import pymem.process as process
from sys import platform
from typing import List
from pymem.macho import Module, Section

class Pymem:
  def __init__(self, process_name: str) -> None:
    assert platform == "darwin", f"pymem-osx only supports MacOS (64-bit ARM), not {platform}"
    self.process_name = process_name
    self.pid = process.get_pid_by_name(process_name)
    assert self.pid != -1, "Failed to find process"
    self.task = process.get_task(self.pid)

  def read_buffer(self, address: int, size: int) -> bytes:
    buffer = ctypes.create_string_buffer(size)
    bytes_read = process.read(self.task, ctypes.c_uint64(address), buffer, size)
    assert bytes_read == size, f"Failed to read buffer, only read {bytes_read} bytes out of {size} bytes"
    return buffer.raw

  def read_int32(self, address: int) -> int: return int.from_bytes(self.read_buffer(address, 4), "little")
  def read_int64(self, address: int) -> int: return int.from_bytes(self.read_buffer(address, 8), "little")
  def read_float(self, address: int) -> float: return ctypes.c_float.from_buffer_copy(self.read_buffer(address, 4)).value
  def read_double(self, address: int) -> float: return ctypes.c_double.from_buffer_copy(self.read_buffer(address, 8)).value
  def read_bool(self, address: int) -> bool: return bool.from_bytes(self.read_buffer(address, 1), "little")

  def write_bytes(self, address: int, buffer: bytes) -> None:
    buffer = ctypes.create_string_buffer(buffer)
    assert process.write(self.task, ctypes.c_uint64(address), buffer, len(buffer)), "Failed to write buffer"

  def write_int32(self, address: int, value: int) -> None: self.write_bytes(address, value.to_bytes(4, "little"))
  def write_int64(self, address: int, value: int) -> None: self.write_bytes(address, value.to_bytes(8, "little"))
  def write_float(self, address: int, value: float) -> None: self.write_bytes(address, ctypes.c_float(value).from_buffer(ctypes.create_string_buffer(4)).raw)
  def write_double(self, address: int, value: float) -> None: self.write_bytes(address, ctypes.c_double(value).from_buffer(ctypes.create_string_buffer(8)).raw)
  def write_bool(self, address: int, value: bool) -> None: self.write_bytes(address, int(value).to_bytes(1, "little"))
  def get_base_address(self) -> int: return process.get_base_address(self.task).value

  def get_modules(self, extended: bool = False) -> List[Module]:
    modules = process.get_modules(self.task)
    if extended: [x.add_sections(process.parse_macho(self.task, x.get_address())) for x in modules]
    return modules
