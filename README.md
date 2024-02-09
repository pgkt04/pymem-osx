# pymem-osx
A python library for MacOS, providing the base functions required for memory manipulation (read/write).

# Features
- Memory read/write helpers.
- Base address searcher
- Modules name and address dumper
- Live in-memory modules macho-o address parser/dumper (x64 implementation).
  - Useful for finding address of different sections (__DATA, __TEXT) and even their respective segments.

# Installation
You can install pymem from source.
```
git clone https://github.com/qtkite/pymem-osx.git
cd pymem-osx
python3 -m pip install -e .
```

Alternatively you can do:
```
pip install pymem-osx
```
# Note
When running your python script, it must be elevated (in sudo mode) for the api calls to work.

# Donate
Buy me a coffee to support some of the work I put out  
[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/B0B65F2OS)
