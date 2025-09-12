# Claude Code Configuration
## Before talking about the project
When you make an output, please try to make the tokens less enough. You do not have to output any comments that can be understood without it.

Please concentrate on generating codes, or making information that are complicated and others.


## Project Overview

This is a RoboCup 2025 Raspberry Pi robotics program for line following and rescue operations. The system uses dual cameras (rescue and line trace), UART communication with microcontrollers, and computer vision for autonomous navigation.

## Architecture

### Core Components

- **main.py**: Main entry point containing the control loop, camera initialization, and high-level robot logic
- **modules/camera.py**: Camera wrapper class for Picamera2 operations with dual camera support
- **modules/uart.py**: UART communication protocol with message-based command/response system
- **modules/settings.py**: Configuration constants including camera settings, thresholds, and detection parameters
- **modules/log.py**: Logging utilities

### Key Systems

- **Dual Camera Setup**: Rescue camera and line trace camera with independent configurations
- **UART Protocol**: Message-based communication system with unique IDs for command/response matching
- **Computer Vision Pipeline**: OpenCV-based image processing for line detection and object recognition
- **Threading**: Thread-safe operations with locks for camera data and global state

## Development Commands

### Code Quality
```bash
# Format code with YAPF (2-space indentation, 80 char limit)
yapf -i -r .

# Lint with pylint
pylint modules/ main.py

# Lint with flake8
flake8 modules/ main.py

# Format with black
black modules/ main.py
```

### Running the Program
```bash
python3 main.py
```

## Code Style Guidelines

- **Formatting**: Uses YAPF with PEP8 base style, 2-space indentation, 80 character line limit (configured in `.style.yapf`)
- **Type Hints**: All functions use type hints with `typing` module
- **Docstrings**: Google-style docstrings for all functions
- **Constants**: Uppercase constants defined in `modules/settings.py`
- **Threading**: Thread-safe operations with proper lock usage

## Commit Guidelines

Follow conventional commit format from `.cursor/rules/commit-rules.mdc`:
- `feat:` New features
- `fix:` Bug fixes  
- `docs:` Documentation changes
- `style:` Code formatting
- `refactor:` Code restructuring
- `perf:` Performance improvements
- `test:` Test changes
- `chore:` Build/tooling changes

First line should be short and descriptive. Leave subsequent lines blank unless you understand the specific reason for the change.

## Dependencies

Core dependencies (see `requirements.txt`):
- `pyserial>=3.5` - UART communication
- `opencv-python>=4.8.0` - Computer vision
- `numpy>=1.24.0` - Numerical operations
- `picamera2>=0.3.12` - Raspberry Pi camera interface
- `libcamera>=0.0.1` - Camera backend

Development tools:
- `pylint>=2.17.0`
- `black>=23.0.0` 
- `flake8>=6.0.0`

## Hardware Integration

- **Cameras**: Dual Picamera2 setup with configurable ports and settings
- **UART**: Serial communication for motor control and sensor readings
- **Sensors**: Ultrasonic distance sensor integration
- **Actuators**: Wire mechanism control for rescue operations

## Configuration

Key settings in `modules/settings.py`:
- Camera ports, sizes, and controls
- Detection thresholds for line following and object recognition
- Debug mode flags
- Threading locks for concurrent operations