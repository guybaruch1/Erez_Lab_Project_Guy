# shared.py

from enum import Enum

# Define the Wavelength enum
class Wavelength(Enum):
    DELTA = 1  # 1-4 Hz
    THETA = 2  # 4-8 Hz
    ALPHA = 3  # 8-12 Hz
    BETA = 4   # 12-30 Hz
    GAMMA = 5  # 30-100 Hz
    HIGH_GAMMA = 6  # 100+ Hz

# You can add more shared constants or utility functions here
