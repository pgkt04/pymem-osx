import ctypes
from ctypes import byref, sizeof, addressof
from typing import List, Tuple

libproc = ctypes.CDLL(ctypes.util.find_library("libproc"))
assert libproc, "Failed to load libproc"

def get_task(process_name): pass