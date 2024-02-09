# this example lists the modules of finder, and reads the magic header
from pymem import PyMem

finder = PyMem("Finder")
modules = finder.get_modules(True)
for i in modules:
  print(i.get_name())
  [print(f"   {x.get_name()} -> {hex(x.get_address())}") for x in i.get_sections()]

# read base address
base_address = finder.get_base_address()
print(hex(base_address))

magic_header = finder.read_int32(base_address)
print(hex(magic_header))
assert magic_header == 0xfeedfacf, "Base address should contain the magic header"