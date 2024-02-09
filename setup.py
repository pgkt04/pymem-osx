#!/usr/bin/env python3

from pathlib import Path
from setuptools import setup

directory = Path(__file__).resolve().parent

with open(directory / 'README.md', encoding='utf-8') as f:
  long_description = f.read()

setup(name="pymem-osx",
      version = "1.0.0",
      description="A MacOS python library for reading and writing memory of other processes",
      author="qtkite",
      license="MIT",
      long_description=long_description,
      long_description_content_type='text/markdown',
      packages=["pymem"],
      python_requires='>=3.8',
      classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
        "Programming Language :: Python :: 3",
      ],
      include_package_data=True)