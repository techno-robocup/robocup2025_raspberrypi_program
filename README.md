# RoboCup 2025 Raspberry Pi Robotics Program

This repository contains the main robotics program for the RoboCup 2025 competition, designed to run on Raspberry Pi hardware with camera and UART communication capabilities.

## Features

- **Dual Camera Support**: Line tracing and rescue cameras with configurable parameters
- **UART Communication**: Serial communication with ESP32 and other external devices
- **Line Following**: Advanced line detection and following algorithms
- **Color Detection**: Green and red mark detection for competition elements
- **Logging System**: Comprehensive logging with Unix timestamps
- **Error Handling**: Robust error handling and recovery mechanisms

## Requirements

- Raspberry Pi (4B recommended)
- Python 3.8 or higher
- Camera modules (compatible with Picamera2)
- UART-capable device (ESP32, Arduino, etc.)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/techno-robocup/robocup2025_raspberrypi_program.git
cd robocup2025_raspberrypi_program
```

### 2. Install Submodules

```bash
git submodule update --init --recursive
```

### 3. Install Dependencies

#### Option A: Using pip (Recommended)

```bash
pip3 install -r requirements.txt
```

#### Option B: Using setup.py

```bash
python3 setup.py install
```

### 4. Verify Installation

```bash
python3 -c "import modules.uart; import modules.log; import modules.camera; import modules.settings; print('All modules imported successfully')"
```

## Usage

### Basic Usage

Run the main program:

```bash
python3 main.py
```

### Configuration

The program uses several configuration files:

- `modules/settings.py`: Camera and algorithm parameters
- `.envrc`: Environment configuration (requires direnv)

### Camera Setup

The program supports two cameras:

1. **Line Tracing Camera** (Port 0): Used for line following
2. **Rescue Camera** (Port 1): Used for rescue operations

Camera parameters can be adjusted in `modules/settings.py`.

### UART Communication

The program communicates with external devices via UART:

- **Baudrate**: 9600 (configurable)
- **Protocol**: ASCII-based message protocol
- **Commands**: Motor control, sensor reading, button status

## Project Structure

```
robocup2025_raspberrypi_program/
├── main.py                 # Main entry point
├── modules/                # Core modules
│   ├── camera.py          # Camera handling
│   ├── uart.py            # UART communication
│   ├── log.py             # Logging system
│   └── settings.py        # Configuration and algorithms
├── requirements.txt        # Python dependencies
├── setup.py               # Installation script
├── fetch.sh               # Sync script (fetch from remote)
├── send.sh                # Sync script (send to remote)
└── README.md              # This file
```

## Development

### Code Style

The project uses:
- **Black**: Code formatting
- **Pylint**: Code linting
- **Type hints**: For better code documentation

### Running Tests

```bash
# Format code
black .

# Lint code
pylint main.py modules/

# Type checking (if mypy is installed)
mypy main.py modules/
```

### Debug Mode

Enable debug mode by setting `DEBUG_MODE = True` in `modules/settings.py`. This will:
- Save debug images to `bin/` directory
- Provide detailed logging
- Show algorithm intermediate results

## Troubleshooting

### Common Issues

1. **Camera not found**: Ensure camera modules are properly connected and enabled
2. **UART communication failed**: Check device connections and permissions
3. **Import errors**: Verify all dependencies are installed
4. **Permission denied**: Run with appropriate permissions for hardware access

### Logs

Logs are saved to `log.log` by default. Check this file for detailed error information.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue on GitHub
- Contact the development team
- Check the project documentation

## Changelog

### Version 1.0.0
- Initial release
- Basic camera and UART functionality
- Line following algorithms
- Color detection capabilities