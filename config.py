"""
Configuration file for RoboCup 2025 Raspberry Pi program.

This file contains all configurable parameters for the robotics program.
"""

import os
from typing import Dict, Any

# Debug settings
DEBUG_MODE = os.getenv('DEBUG_MODE', 'True').lower() == 'true'

# Image processing settings
BLACK_WHITE_THRESHOLD = int(os.getenv('BLACK_WHITE_THRESHOLD', '125'))
MIN_GREEN_AREA = int(os.getenv('MIN_GREEN_AREA', '500'))
MIN_RED_AREA = int(os.getenv('MIN_RED_AREA', '500'))

# Camera settings
LINETRACE_CAMERA_PORT = int(os.getenv('LINETRACE_CAMERA_PORT', '0'))
RESCUE_CAMERA_PORT = int(os.getenv('RESCUE_CAMERA_PORT', '1'))

# Image dimensions
LINETRACE_CAMERA_LORES_WIDTH = int(os.getenv('LINETRACE_CAMERA_LORES_WIDTH', '320'))
LINETRACE_CAMERA_LORES_HEIGHT = int(os.getenv('LINETRACE_CAMERA_LORES_HEIGHT', '180'))

# UART settings
UART_BAUDRATE = int(os.getenv('UART_BAUDRATE', '9600'))
UART_TIMEOUT = float(os.getenv('UART_TIMEOUT', '1.0'))

# Algorithm settings
COMPUTING_P = float(os.getenv('COMPUTING_P', '1.0'))

# File paths
LOG_FILE = os.getenv('LOG_FILE', 'log.log')
DEBUG_IMAGE_DIR = os.getenv('DEBUG_IMAGE_DIR', 'bin')

# Timeout settings
UART_SEND_TIMEOUT = float(os.getenv('UART_SEND_TIMEOUT', '1.0'))
UART_RECEIVE_TIMEOUT = float(os.getenv('UART_RECEIVE_TIMEOUT', '1.0'))

# Motor control settings
MOTOR_MIN_SPEED = int(os.getenv('MOTOR_MIN_SPEED', '-255'))
MOTOR_MAX_SPEED = int(os.getenv('MOTOR_MAX_SPEED', '255'))

# Line following settings
LINE_WIDTH_THRESHOLD = int(os.getenv('LINE_WIDTH_THRESHOLD', '20'))
LINE_DISTANCE_PENALTY = int(os.getenv('LINE_DISTANCE_PENALTY', '30'))

# Color detection settings
GREEN_HSV_LOWER = [35, 60, 0]
GREEN_HSV_UPPER = [85, 255, 255]

RED_HSV_LOWER_1 = [0, 40, 0]
RED_HSV_UPPER_1 = [30, 255, 255]
RED_HSV_LOWER_2 = [100, 40, 0]
RED_HSV_UPPER_2 = [180, 255, 255]

# Camera controls (can be overridden by environment variables)
def get_camera_controls() -> Dict[str, Dict[str, Any]]:
    """Get camera control settings."""
    return {
        'linetrace': {
            'AfMode': 'Manual',
            'LensPosition': 1.0 / 0.03,
            'AeFlickerMode': 'Manual',
            'AeFlickerPeriod': 10000,
            'AeMeteringMode': 'Matrix',
            'AwbEnable': False,
            'AwbMode': 'Indoor',
            'HdrMode': 'Night'
        },
        'rescue': {
            'AfMode': 'Continuous',
            'AfSpeed': 'Fast',
            'AeFlickerMode': 'Manual',
            'AeFlickerPeriod': 10000,
            'AeMeteringMode': 'Matrix',
            'AwbEnable': True,
            'AwbMode': 'Indoor',
            'HdrMode': 'Off'
        }
    }

# Validation functions
def validate_config() -> bool:
    """Validate configuration settings."""
    errors = []
    
    if not (0 <= LINETRACE_CAMERA_PORT <= 1):
        errors.append("LINETRACE_CAMERA_PORT must be 0 or 1")
    
    if not (0 <= RESCUE_CAMERA_PORT <= 1):
        errors.append("RESCUE_CAMERA_PORT must be 0 or 1")
    
    if LINETRACE_CAMERA_PORT == RESCUE_CAMERA_PORT:
        errors.append("LINETRACE_CAMERA_PORT and RESCUE_CAMERA_PORT must be different")
    
    if not (0 <= BLACK_WHITE_THRESHOLD <= 255):
        errors.append("BLACK_WHITE_THRESHOLD must be between 0 and 255")
    
    if UART_BAUDRATE <= 0:
        errors.append("UART_BAUDRATE must be positive")
    
    if errors:
        print("Configuration errors:")
        for error in errors:
            print(f"  - {error}")
        return False
    
    return True

# Print configuration summary
def print_config_summary():
    """Print a summary of the current configuration."""
    print("=== Configuration Summary ===")
    print(f"Debug Mode: {DEBUG_MODE}")
    print(f"Line Trace Camera Port: {LINETRACE_CAMERA_PORT}")
    print(f"Rescue Camera Port: {RESCUE_CAMERA_PORT}")
    print(f"UART Baudrate: {UART_BAUDRATE}")
    print(f"Black/White Threshold: {BLACK_WHITE_THRESHOLD}")
    print(f"Min Green Area: {MIN_GREEN_AREA}")
    print(f"Min Red Area: {MIN_RED_AREA}")
    print(f"Computing P: {COMPUTING_P}")
    print(f"Log File: {LOG_FILE}")
    print(f"Debug Image Directory: {DEBUG_IMAGE_DIR}")
    print("============================")

if __name__ == "__main__":
    print_config_summary()
    if validate_config():
        print("✓ Configuration is valid")
    else:
        print("✗ Configuration has errors")