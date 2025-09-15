# RoboCup 2025 Raspberry Pi Program Overview

## Project Purpose
RoboCup 2025 Raspberry Pi robotics program for line following and rescue operations using computer vision and autonomous navigation.

## Core Architecture

### Main Components
- **main.py**: Main entry point with control loop, camera initialization, and high-level robot logic
- **modules/camera.py**: Camera wrapper for Picamera2 operations with dual camera support
- **modules/uart.py**: UART communication protocol with message-based command/response system
- **modules/settings.py**: Configuration constants (camera settings, thresholds, detection parameters)
- **modules/log.py**: Logging utilities

### Key Systems
- **Dual Camera Setup**: Rescue camera + line trace camera with independent configs
- **UART Protocol**: Message-based communication with unique IDs for command/response matching
- **Computer Vision**: OpenCV-based image processing for line detection and object recognition
- **Threading**: Thread-safe operations with locks for camera data and global state

## Development Workflow

### Code Quality Commands
```bash
yapf -i -r .          # Format (2-space indent, 80 char limit)
pylint modules/ main.py
flake8 modules/ main.py
black modules/ main.py
python3 main.py       # Run program
```

### Code Style
- YAPF formatting with PEP8, 2-space indentation, 80 char limit
- Type hints with `typing` module
- Google-style docstrings
- Uppercase constants in `modules/settings.py`
- Thread-safe operations with proper locks

### Commit Format
Conventional commits: `feat:`, `fix:`, `docs:`, `style:`, `refactor:`, `perf:`, `test:`, `chore:`

## Key Dependencies
- `pyserial>=3.5` - UART communication
- `opencv-python>=4.8.0` - Computer vision
- `numpy>=1.24.0` - Numerical operations
- `picamera2>=0.3.12` - Raspberry Pi camera interface
- `libcamera>=0.0.1` - Camera backend

## Hardware Integration
- Dual Picamera2 setup with configurable ports
- Serial communication for motor control and sensor readings
- Ultrasonic distance sensor integration
- Wire mechanism control for rescue operations

## Configuration
Key settings in `modules/settings.py` include camera ports/sizes/controls, detection thresholds, debug flags, and threading locks.