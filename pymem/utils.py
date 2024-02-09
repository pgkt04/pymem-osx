import ctypes

def align_address(addr: ctypes.c_uint64, full_size: bool = False) -> ctypes.c_uint64:
  alignment = 0x4000 if full_size else 0x1000
  return ctypes.c_uint64((addr.value // alignment) * alignment + (alignment if full_size else 0))