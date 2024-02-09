from ctypes import c_uint64, c_uint32
from platform import architecture

if architecture()[0] == "64bit":
  uintptr_t = c_uint64
else:
  uintptr_t = c_uint32