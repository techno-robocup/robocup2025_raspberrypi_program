#!/usr/bin/env python3
"""
Setup script for RoboCup 2025 Raspberry Pi robotics program.

This script handles installation of dependencies and project setup.
"""

from setuptools import setup, find_packages
import os


# Read requirements from requirements.txt
def read_requirements():
  """Read requirements from requirements.txt file."""
  requirements = []
  if os.path.exists('requirements.txt'):
    with open('requirements.txt', 'r') as f:
      for line in f:
        line = line.strip()
        if line and not line.startswith('#'):
          requirements.append(line)
  return requirements


# Read README for long description
def read_readme():
  """Read README file for long description."""
  if os.path.exists('README.md'):
    with open('README.md', 'r', encoding='utf-8') as f:
      return f.read()
  return "RoboCup 2025 Raspberry Pi robotics program"


setup(
    name="robocup2025-raspberrypi",
    version="1.0.0",
    description="RoboCup 2025 Raspberry Pi robotics program",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    author="RoboCup Team",
    author_email="team@robocup2025.com",
    url="https://github.com/techno-robocup/robocup2025_raspberrypi_program",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=read_requirements(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: System :: Hardware",
    ],
    entry_points={
        "console_scripts": [
            "robocup2025=main:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
