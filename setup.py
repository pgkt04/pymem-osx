#!/usr/bin/env python3

from pathlib import Path
from setuptools import setup

directory = Path(__file__).resolve().parent

with open(directory / 'README.md', encoding='utf-8') as f:
  long_description = f.read()

setup(name="pymem-osx",
      version = "1.0.4",
      description="A Python library for reading and writing process memory on macOS using Mach kernel APIs",
      author="pgkt04",
      license="MIT",
      long_description=long_description,
      long_description_content_type='text/markdown',
      packages=["pymem", "pymem.resources"],
      python_requires='>=3.8',
      keywords=[
        "memory", "macos", "osx", "process", "mach",
        "read-memory", "write-memory", "ctypes",
        "pymem", "mach-o", "macho", "dylib",
        "reverse-engineering", "game-hacking",
        "apple-silicon", "arm64", "m1",
        "task-for-pid", "memory-manipulation",
      ],
      classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
        "Operating System :: MacOS :: MacOS X",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries",
        "Topic :: System :: Operating System Kernels :: BSD",
        "Topic :: Security",
        "Intended Audience :: Developers",
        "Development Status :: 5 - Production/Stable",
      ],
      url="https://github.com/pgkt04/pymem-osx",
      project_urls={
        "Source Code": "https://github.com/pgkt04/pymem-osx"
      },
      include_package_data=True)
