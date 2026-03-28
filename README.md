# pymem-osx

A Python library for **reading and writing process memory on macOS**. Provides a clean interface for cross-process memory manipulation using Mach kernel APIs — no compiled extensions, no dependencies, pure Python via `ctypes`.

Built for **Apple Silicon (M1/M2/M3)** and 64-bit macOS. If you've used [pymem](https://github.com/srounet/Pymem) on Windows, this is the macOS equivalent.

## Features

- **Read/write process memory** — int32, int64, float, double, bool, raw bytes
- **Find processes by name** — enumerate PIDs, resolve to Mach task ports
- **Get base address** of any running process
- **Enumerate loaded modules** — list all dylibs/frameworks loaded in a process
- **Parse Mach-O headers in-memory** — extract segments (`__TEXT`, `__DATA`) and their sections from live processes
- **Zero dependencies** — pure Python, uses `ctypes` to call `libproc` directly

## Installation

```bash
pip install pymem-osx
```

Or from source:

```bash
git clone https://github.com/pgkt04/pymem-osx.git
cd pymem-osx
pip install -e .
```

## Requirements

- **macOS** (Apple Silicon or Intel 64-bit)
- **Python 3.8+**
- **Root privileges** — must run with `sudo` (required by `task_for_pid`)

## Quick Start

```python
from pymem import Pymem

# Attach to a running process
pm = Pymem("Finder")

# Read the base address
base = pm.get_base_address()
print(f"Base address: {hex(base)}")

# Read the Mach-O magic header
magic = pm.read_int32(base)
print(f"Magic: {hex(magic)}")  # 0xfeedfacf

# Read/write memory
value = pm.read_int64(some_address)
pm.write_int64(some_address, 42)
```

Run with sudo:

```bash
sudo python3 your_script.py
```

## Enumerating Modules

List all loaded dylibs and their Mach-O sections:

```python
from pymem import Pymem

pm = Pymem("Finder")

# extended=True parses Mach-O headers for each module
modules = pm.get_modules(extended=True)

for module in modules:
    print(module.get_name())
    for section in module.get_sections():
        print(f"  {section.get_name()} -> {hex(section.get_address())}")
```

## API Reference

### Pymem

| Method | Description |
|--------|-------------|
| `Pymem(process_name)` | Attach to a process by name |
| `read_bytes(address, size)` | Read raw bytes |
| `read_int32(address)` | Read 4-byte integer |
| `read_int64(address)` | Read 8-byte integer |
| `read_float(address)` | Read 4-byte float |
| `read_double(address)` | Read 8-byte double |
| `read_bool(address)` | Read boolean |
| `write_bytes(address, buffer)` | Write raw bytes |
| `write_int32(address, value)` | Write 4-byte integer |
| `write_int64(address, value)` | Write 8-byte integer |
| `write_float(address, value)` | Write 4-byte float |
| `write_double(address, value)` | Write 8-byte double |
| `write_bool(address, value)` | Write boolean |
| `get_base_address()` | Get process base virtual address |
| `get_modules(extended=False)` | List loaded modules/dylibs |

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `process_name` | `str` | Target process name |
| `pid` | `int` | Process ID |
| `task` | `c_uint64` | Mach task port |

### Data Models

- **`Module`** — a loaded dylib/framework (name, address, sections)
- **`Section`** — a Mach-O segment like `__TEXT` or `__DATA` (name, address, child segments)
- **`Segment`** — a Mach-O section like `__got` or `__la_symbol_ptr` (name, address)

## How It Works

pymem-osx calls macOS Mach kernel APIs through `ctypes` and `libproc`:

- `task_for_pid()` — obtain a Mach task port for the target process
- `mach_vm_read_overwrite()` / `mach_vm_write()` — read/write process memory
- `mach_vm_protect()` — change memory protection flags
- `mach_vm_region()` — scan virtual memory regions
- `task_info()` — query `dyld_all_image_infos` for loaded module enumeration

No compiled C extensions are needed — everything goes through Python's built-in `ctypes`.
