from ctypes import c_uint64, c_uint32
from platform import architecture

uintptr_t = c_uint64 if architecture()[0] == "64bit" else c_uint32