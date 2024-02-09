import ctypes, os
from ctypes import byref, sizeof, addressof, util
from typing import List, Tuple
from pymem.resources import vmtypes as vt
from pymem.utils import align_address
from pymem.macho import Segment, Section, Module

libproc = ctypes.CDLL(ctypes.util.find_library("libproc"))
assert libproc, "Failed to load libproc"

def get_all_pids() -> List[int]:
  pids = (ctypes.c_int * vt.NUM_PIDS)()
  num_pids_returned = libproc.proc_listpids(vt.PROC_ALL_PIDS, 0, pids, sizeof(pids))
  if num_pids_returned <= 0: return []
  return pids[:num_pids_returned]

def get_pid_by_name(name: str, case_sensitive: bool = False) -> int:
  all_pids = get_all_pids()
  if len(all_pids) <= 0: return -1
  for pid in all_pids:
    if pid == 0: continue
    path_buffer = ctypes.create_string_buffer(vt.PROC_PIDPATHINFO_MAXSIZE)
    ret = libproc.proc_pidpath(pid, path_buffer, sizeof(path_buffer))
    if ret > 0:
      path = path_buffer.value.decode()
      _, proc_name = os.path.split(path)
      if case_sensitive:
        if proc_name == name: return pid
      else:
        if proc_name.lower() == name.lower(): return pid
  return -1

def get_task(pid: int) -> ctypes.c_uint64:
  task = ctypes.c_uint64()
  current_task = libproc.mach_task_self()
  kern = ctypes.c_int(libproc.task_for_pid(current_task, pid, ctypes.byref(task)))
  assert kern.value == 0, f"task_for_pid failed with error {kern}"
  return task

def get_base_address(task: int, prot_level: ctypes.c_uint32 = (vt.VM_PROT_EXECUTE | vt.VM_PROT_READ | vt.VM_PROT_WRITE), strict: bool = False) -> ctypes.c_uint64:
  addr = ctypes.c_uint64()
  size = ctypes.c_uint32()
  count = ctypes.c_uint32(vt.VM_REGION_BASIC_INFO_COUNT_64)
  info = vt.VmRegionBasicInfo64()
  obj_name = ctypes.c_uint32()
  while True:
    kern = ctypes.c_int(libproc.mach_vm_region(task, ctypes.byref(addr), ctypes.byref(size), vt.VM_REGION_BASIC_INFO_64, ctypes.byref(info), ctypes.byref(count), ctypes.byref(obj_name)))
    if kern.value != 0:
      print(f"mach_vm_region failed with error {kern}")
      return -1
    if strict:
      if info.protection == prot_level: return addr
    else:
      if info.protection & prot_level: return addr
    addr.value += size.value

def read(task: int, addr: ctypes.c_uint64, buffer: ctypes.Array, size: int) -> int:
  read_size = ctypes.c_uint64(0)
  kret = ctypes.c_int(libproc.mach_vm_read_overwrite(task, addr, size, ctypes.cast(buffer, ctypes.c_void_p), ctypes.byref(read_size)))
  if kret.value != 0:
    print(f"mach_vm_read_overwrite failed with error {kret}")
    return -1
  return read_size.value

def write(task: int, addr: ctypes.c_uint64, buffer: ctypes.Array, size: int) -> bool:
  kret = ctypes.c_int(libproc.mach_vm_write(task, addr, ctypes.cast(buffer, ctypes.c_void_p), size))
  if kret.value != 0:
    print(f"mach_vm_write failed with error {kret}")
    return False
  return True

def change_protection(task: int, addr: ctypes.c_uint64, size: int, protection: int) -> bool:
  set_maximum = ctypes.c_bool(False)
  kret = libproc.mach_vm_protect(task, align_address(addr), size, set_maximum, protection)
  if kret != 0:
    print(f"mach_vm_protect failed with error {kret}")
    return False
  return True

def get_protection(task: int, addr: ctypes.c_uint64) -> int:
  size = ctypes.c_uint32()
  count = ctypes.c_uint32(vt.VM_REGION_BASIC_INFO_COUNT_64)
  info = vt.VmRegionBasicInfo64()
  obj_name = ctypes.c_uint32()
  aligned_addr = align_address(addr)
  kern = ctypes.c_int(libproc.mach_vm_region(task, ctypes.byref(aligned_addr), byref(size), vt.VM_REGION_BASIC_INFO_64, byref(info), byref(count), byref(obj_name)))
  if kern.value != 0:
    print(f"mach_vm_region failed with error {kern}")
    return -1
  return info.protection

def get_modules(task: int) -> List[Module]:
  # read task_dyld_info
  dyld_info = vt.task_dyld_info()
  count = ctypes.c_uint32(vt.TASK_DYLD_INFO_COUNT)
  kern = ctypes.c_int(libproc.task_info(task, vt.TASK_DYLD_INFO, ctypes.byref(dyld_info), ctypes.byref(count)))
  if kern.value != 0:
    print(f"task_info failed with error {kern}")
    return []

  SIZE_DYLD_ALL_IMAGE_INFOS = sizeof(vt.dyld_all_image_infos)

  # read dyld_all_image_infos
  buffer = ctypes.create_string_buffer(SIZE_DYLD_ALL_IMAGE_INFOS)
  res = read(task, ctypes.c_uint64(dyld_info.all_image_info_addr), buffer, SIZE_DYLD_ALL_IMAGE_INFOS)
  if res <= 0:
    print(f"Failed to read dyld_all_image_infos")
    return []
  all_image_infos = ctypes.cast(buffer, ctypes.POINTER(vt.dyld_all_image_infos)).contents

  # read dyld_image_info array
  size = all_image_infos.infoArrayCount * sizeof(vt.dyld_image_info)
  buffer = ctypes.create_string_buffer(size)
  res = read(task, ctypes.c_uint64(all_image_infos.infoArray), buffer, size)
  if res <= 0:
    print(f"Failed to read dyld_image_info array")
    return []
  image_info_array: vt.dyld_image_info = ctypes.cast(buffer, ctypes.POINTER(vt.dyld_image_info * all_image_infos.infoArrayCount)).contents
  modules = []

  for i in range(all_image_infos.infoArrayCount):
    info: vt.dyld_image_info = image_info_array[i]
    buffer = ctypes.create_string_buffer(1024)
    read(task, ctypes.c_uint64(info.imageFilePath), buffer, len(buffer))
    modules.append(Module(buffer.value.decode(), info.imageLoadAddress))

  # also add dyld itself
  all_image_infos.dyldPath
  buffer = ctypes.create_string_buffer(1024)
  res = read(task, ctypes.c_uint64(all_image_infos.dyldPath), buffer, len(buffer))
  assert res > 0, f"Failed to read dyld path"
  modules.append(Module(buffer.value.decode(), all_image_infos.dyldImageLoadAddress))
  return modules

# currently only parses mach64 since we only interested in macos m1
def parse_macho(task: int, base_addr: int) -> List[Section]:
  ret = []
  addr = ctypes.c_uint64(base_addr)
  header_size = sizeof(vt.mach_header_64)
  buffer = ctypes.create_string_buffer(header_size)
  result = read(task, addr, buffer, header_size)
  assert result == header_size, f"Failed to read {header_size} bytes"
  header: vt.mach_header_64 = ctypes.cast(buffer, ctypes.POINTER(vt.mach_header_64)).contents
  if header.magic == vt.MH_MAGIC_64:
    cmd_buffer = ctypes.create_string_buffer(header.sizeofcmds)
    result = read(task, ctypes.c_uint64(addr.value + header_size), cmd_buffer, header.sizeofcmds)
    assert result == header.sizeofcmds, f"Failed to read {header.sizeofcmds} bytes, only read {result}"
    offset = 0
    addr_rebase = 0
    for _ in range(header.ncmds): # parse each load command
      command_addr = addressof(cmd_buffer) + offset
      load_cmd: vt.load_comand = ctypes.cast(command_addr, ctypes.POINTER(vt.load_command)).contents
      if load_cmd.cmd == vt.LC_SEGMENT_64:
        segment_64: vt.segment_command_64 = ctypes.cast(addressof(cmd_buffer) + offset, ctypes.POINTER(vt.segment_command_64)).contents
        if offset == 0:
          addr_rebase = abs(segment_64.vmaddr - addr.value)
          segment_64.vmaddr = addr.value
        else:
          segment_64.vmaddr += addr_rebase
        segments = []
        for i in range(segment_64.nsects): # parse sections
          section: vt.section_64 = ctypes.cast(command_addr + sizeof(vt.segment_command_64) + (i * sizeof(vt.section_64)), ctypes.POINTER(vt.section_64)).contents
          section.addr += addr_rebase
          segments.append(Segment(section.sectname.decode(), section.addr))
        ret.append(Section(segment_64.segname.decode(), segment_64.vmaddr, segments))
      offset += load_cmd.cmdsize # moves to next load command
  return ret