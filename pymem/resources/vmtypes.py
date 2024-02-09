import ctypes

class VmRegionBasicInfo64(ctypes.Structure):
  _fields_ = [
    ("protection", ctypes.c_uint32),
    ("max_protection", ctypes.c_uint32),
    ("inheritance", ctypes.c_uint32),
    ("shared", ctypes.c_uint32),
    ("reserved", ctypes.c_uint32),
    ("offset", ctypes.c_uint64),
    ("behavior", ctypes.c_uint32),
    ("user_wired_count", ctypes.c_ushort)
  ]
  protection: ctypes.c_uint32
  max_protection: ctypes.c_uint32
  inheritance: ctypes.c_uint32
  shared: ctypes.c_uint32
  reserved: ctypes.c_uint32
  offset: ctypes.c_uint64
  behavior: ctypes.c_uint32
  user_wired_count: ctypes.c_ushort


class task_dyld_info(ctypes.Structure):
  _fields_ = [
    ("all_image_info_addr", ctypes.c_uint64),
    ("all_image_info_size", ctypes.c_uint64),
    ("all_image_info_format", ctypes.c_int32)
  ]
  all_image_info_addr: ctypes.c_uint64
  all_image_info_size: ctypes.c_uint64
  all_image_info_format: ctypes.c_int32

TASK_DYLD_INFO_COUNT = ctypes.sizeof(task_dyld_info) // ctypes.sizeof(ctypes.c_int32) # 5?
TASK_DYLD_INFO = 17

VM_PROT_NONE = 0x00
VM_PROT_READ = 0x01
VM_PROT_WRITE = 0x02
VM_PROT_EXECUTE = 0x04
VM_PROT_COPY = 0x08

PROC_ALL_PIDS = 1
PROC_PIDPATHINFO_MAXSIZE = 1024*4
NUM_PIDS = 1024
VM_REGION_BASIC_INFO_64 = 9
VM_REGION_BASIC_INFO_COUNT_64 = 9

DYLD_MAX_PROCESS_INFO_NOTIFY_COUNT = 8

class dyld_all_image_infos(ctypes.Structure):
  _fields_ = [
    ("version", ctypes.c_uint32),
    ("infoArrayCount", ctypes.c_uint32),
    ("infoArray", ctypes.c_void_p), # dyld_image_info ptr
    ("notification", ctypes.c_uint64),
    ("processDetachedFromSharedRegion", ctypes.c_uint8),
    #	the following fields are only in version 2 (Mac OS X 10.6, iPhoneOS 2.0) and later
    ("libSystemInitialized", ctypes.c_uint8),
    ("dyldImageLoadAddress", ctypes.c_uint64), # a mach_header pointer
    # the following field is only in version 3 (Mac OS X 10.6, iPhoneOS 3.0) and later
    ("jitInfo", ctypes.c_void_p),
    # the following fields are only in version 5 (Mac OS X 10.6, iPhoneOS 3.0) and later
    ("dyldVersion", ctypes.c_char_p),
    ("errorMessage", ctypes.c_char_p),
    ("terminationFlags", ctypes.c_uint64),
   	# the following field is only in version 6 (Mac OS X 10.6, iPhoneOS 3.1) and later
    ("coreSymbolicationShmPage", ctypes.c_void_p),
    # the following field is only in version 7 (Mac OS X 10.6, iPhoneOS 3.1) and later
    ("systemOrderFlag", ctypes.c_uint64),
    # the following field is only in version 8 (Mac OS X 10.7, iPhoneOS 3.1) and later
    ("uuidArrayCount", ctypes.c_uint64),
    ("uuidArray", ctypes.c_void_p), # dyld_uuid_info ptr, only images not in dyld shared cache
    # the following field is only in version 9 (Mac OS X 10.7, iOS 4.0) and later
    ("dyldAllImageInfosAddress", ctypes.c_void_p), # dyld_all_image_infos ptr, only in version 9 (Mac OS X 10.7, iOS 4.0) and later
    # the following field is only in version 10 (Mac OS X 10.7, iOS 4.2) and later
    ("initialImageCount", ctypes.c_uint64),
    # the following field is only in version 11 (Mac OS X 10.7, iOS 4.2) and later
    ("errorKind", ctypes.c_uint64),
    ("errorClientOfDylibPath", ctypes.c_char_p),
    ("errorTargetDylibPath", ctypes.c_char_p),
    ("errorSymbol", ctypes.c_char_p),
    # the following field is only in version 12 (Mac OS X 10.7, iOS 4.3) and later
    ("sharedCacheSlide", ctypes.c_uint64),
    # the following field is only in version 13 (Mac OS X 10.9, iOS 7.0) and later
    ("sharedCacheUUID", ctypes.c_uint8 * 16),
    # the following field is only in version 15 (macOS 10.12, iOS 10.0) and later
    ("sharedCacheBaseAddress", ctypes.c_uint64),
    ("infoArrayChangeTimestamp", ctypes.c_uint64),
    ("dyldPath", ctypes.c_uint64), # c_char_p, but casted to get address easier
    ("notifyPorts", ctypes.c_uint32 * DYLD_MAX_PROCESS_INFO_NOTIFY_COUNT),
    # if __LP64__, otherwise its 1
    # ("reserved", ctypes.c_uint64 * 11-(DYLD_MAX_PROCESS_INFO_NOTIFY_COUNT//2)),
    ("reserved", ctypes.c_uint64 * 7),
    # The following fields were added in version 18 (previously they were reserved padding fields)
    ("sharedCacheFSID", ctypes.c_uint64),
    ("sharedCacheFSObjID", ctypes.c_uint64),
    # the following field is only in version 16 (macOS 10.13, iOS 11.0) and later
    ("compact_dyld_image_info_addr", ctypes.c_uint64),
    ("compact_dyld_image_info_size", ctypes.c_uint64),
    ("platform", ctypes.c_uint32), # FIXME: really a dyld_platform_t, but those aren't exposed here.
    # the following field is only in version 17 (macOS 10.16) and later
    ("aotInfoCount", ctypes.c_uint32),
    ("aotInfoArray", ctypes.c_uint64), # dyld_aot_image_info ptr
    ("aotInfoArrayChangeTimestamp", ctypes.c_uint64),
    ("aotSharedCacheBaseAddress", ctypes.c_uint64),
    ("aotSharedCacheUUID", ctypes.c_uint8 * 16),
  ]
  version: ctypes.c_uint32
  infoArrayCount: ctypes.c_uint32
  infoArray: ctypes.c_void_p
  notification: ctypes.c_uint64
  processDetachedFromSharedRegion: ctypes.c_uint8
  libSystemInitialized: ctypes.c_uint8
  dyldImageLoadAddress: ctypes.c_uint64
  jitInfo: ctypes.c_void_p
  dyldVersion: ctypes.c_char_p
  errorMessage: ctypes.c_char_p
  terminationFlags: ctypes.c_uint64
  coreSymbolicationShmPage: ctypes.c_void_p
  systemOrderFlag: ctypes.c_uint64
  uuidArrayCount: ctypes.c_uint64
  uuidArray: ctypes.c_void_p
  dyldAllImageInfosAddress: ctypes.c_void_p
  initialImageCount: ctypes.c_uint64
  errorKind: ctypes.c_uint64
  errorClientOfDylibPath: ctypes.c_char_p
  errorTargetDylibPath: ctypes.c_char_p
  errorSymbol: ctypes.c_char_p
  sharedCacheSlide: ctypes.c_uint64
  sharedCacheUUID: ctypes.c_uint8 * 16
  sharedCacheBaseAddress: ctypes.c_uint64
  infoArrayChangeTimestamp: ctypes.c_uint64
  dyldPath: ctypes.c_uint64
  notifyPorts: ctypes.c_uint32 * DYLD_MAX_PROCESS_INFO_NOTIFY_COUNT
  reserved: ctypes.c_uint64 * 7
  sharedCacheFSID: ctypes.c_uint64
  sharedCacheFSObjID: ctypes.c_uint64
  compact_dyld_image_info_addr: ctypes.c_uint64
  compact_dyld_image_info_size: ctypes.c_uint64
  platform: ctypes.c_uint32
  aotInfoCount: ctypes.c_uint32
  aotInfoArray: ctypes.c_uint64
  aotInfoArrayChangeTimestamp: ctypes.c_uint64
  aotSharedCacheBaseAddress: ctypes.c_uint64
  aotSharedCacheUUID: ctypes.c_uint8 * 16


# include/mach-o/dyld_images.h
class dyld_image_info(ctypes.Structure):
  _fields_ = [
    ("imageLoadAddress", ctypes.c_void_p),
    ("imageFilePath", ctypes.c_uint64),     # c_char_p, but casted to get address easier
    ("imageFileModDate", ctypes.c_uint64),
  ]
  imageLoadAddress: ctypes.c_void_p
  imageFilePath: ctypes.c_char_p
  imageFileModDate: ctypes.c_uint64


# include/mach-o/loader.h
class mach_header_64(ctypes.Structure):
  _fields_ = [
    ("magic", ctypes.c_uint32),
    ("cputype", ctypes.c_int32),
    ("cpusubtype", ctypes.c_int32),
    ("filetype", ctypes.c_uint32),
    ("ncmds", ctypes.c_uint32),
    ("sizeofcmds", ctypes.c_uint32),
    ("flags", ctypes.c_uint32),
    ("reserved", ctypes.c_uint32)
  ]
  magic: ctypes.c_uint32
  cputype: ctypes.c_int32
  cpusubtype: ctypes.c_int32
  filetype: ctypes.c_uint32
  ncmds: ctypes.c_uint32
  sizeofcmds: ctypes.c_uint32
  flags: ctypes.c_uint32
  reserved: ctypes.c_uint32

MH_MAGIC_64 = 0xfeedfacf
MH_CIGAM_64 = 0xcffaedfe

# include/mach-o/loader.h
class load_command(ctypes.Structure):
  _fields_ = [
    ("cmd", ctypes.c_uint32),
    ("cmdsize", ctypes.c_uint32)
  ]
  cmd: ctypes.c_uint32
  cmdsize: ctypes.c_uint32

LC_SEGMENT_64 = 0x19
class segment_command_64(ctypes.Structure):
  _fields_ = [
    ("cmd", ctypes.c_uint32),
    ("cmdsize", ctypes.c_uint32),
    ("segname", ctypes.c_char * 16),
    ("vmaddr", ctypes.c_uint64),
    ("vmsize", ctypes.c_uint64),
    ("fileoff", ctypes.c_uint64),
    ("filesize", ctypes.c_uint64),
    ("maxprot", ctypes.c_int32),
    ("initprot", ctypes.c_int32),
    ("nsects", ctypes.c_uint32),
    ("flags", ctypes.c_uint32)
  ]
  cmd: ctypes.c_uint32
  cmdsize: ctypes.c_uint32
  segname: ctypes.c_char * 16
  vmaddr: ctypes.c_uint64
  vmsize: ctypes.c_uint64
  fileoff: ctypes.c_uint64
  filesize: ctypes.c_uint64
  maxprot: ctypes.c_int32
  initprot: ctypes.c_int32
  nsects: ctypes.c_uint32
  flags: ctypes.c_uint32

class section(ctypes.Structure):
  _fields_ = [
    ("sectname", ctypes.c_char * 16),
    ("segname", ctypes.c_char * 16),
    ("addr", ctypes.c_uint32),
    ("size", ctypes.c_uint32),
    ("offset", ctypes.c_uint32),
    ("align", ctypes.c_uint32),
    ("reloff", ctypes.c_uint32),
    ("nreloc", ctypes.c_uint32),
    ("flags", ctypes.c_uint32),
    ("reserved1", ctypes.c_uint32),
    ("reserved2", ctypes.c_uint32),
  ]
  sectname: ctypes.c_char * 16
  segname: ctypes.c_char * 16
  addr: ctypes.c_uint32
  size: ctypes.c_uint32
  offset: ctypes.c_uint32
  align: ctypes.c_uint32
  reloff: ctypes.c_uint32
  nreloc: ctypes.c_uint32
  flags: ctypes.c_uint32
  reserved1: ctypes.c_uint32
  reserved2: ctypes.c_uint32

class section_64(ctypes.Structure):
  _fields_ = [
    ("sectname", ctypes.c_char * 16),
    ("segname", ctypes.c_char * 16),
    ("addr", ctypes.c_uint64),
    ("size", ctypes.c_uint64),
    ("offset", ctypes.c_uint32),
    ("align", ctypes.c_uint32),
    ("reloff", ctypes.c_uint32),
    ("nreloc", ctypes.c_uint32),
    ("flags", ctypes.c_uint32),
    ("reserved1", ctypes.c_uint32),
    ("reserved2", ctypes.c_uint32),
    ("reserved3", ctypes.c_uint32)
  ]
  sectname: ctypes.c_char * 16
  segname: ctypes.c_char * 16
  addr: ctypes.c_uint64
  size: ctypes.c_uint64
  offset: ctypes.c_uint32
  align: ctypes.c_uint32
  reloff: ctypes.c_uint32
  nreloc: ctypes.c_uint32
  flags: ctypes.c_uint32
  reserved1: ctypes.c_uint32
  reserved2: ctypes.c_uint32
  reserved3: ctypes.c_uint32