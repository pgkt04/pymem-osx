# from pymem import process
from sys import platform

class PyMem:
  def __init__(self, process_name: str) -> None:
    self.task = 0
    self.process_name = process_name
    print(platform)
  def read_buffer(self, address: int, size: int) -> bytes: pass
  def read_int(self, address: int) -> int: pass
  def read_float(self, address: int) -> float: pass
  def read_double(self, address: int) -> float: pass
  def read_bool(self, address: int) -> bool: pass
  def read_bytes(self, address: int, size: int) -> bytes: pass
  def write_buffer(self, address: int, buffer: bytes) -> None: pass
  def write_int(self, address: int, value: int) -> None: pass
  def write_float(self, address: int, value: float) -> None: pass
  def write_double(self, address: int, value: float) -> None: pass
  def write_bool(self, address: int, value: bool) -> None: pass
  def get_modules(self) -> list: pass