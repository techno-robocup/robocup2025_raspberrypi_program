# RoboCup 2025 Raspberry Pi Robotics Program

A comprehensive robotics program designed for RoboCup 2025 competition, featuring line following, rescue operations, and ultrasonic sensor integration on Raspberry Pi hardware.

## 🚀 Features

- **Line Following**: Advanced line detection and following algorithms
- **Rescue Operations**: Camera-based rescue mission capabilities
- **UART Communication**: Real-time communication with motor controllers
- **Ultrasonic Sensing**: Distance measurement for obstacle detection
- **Dual Camera System**: Separate cameras for line tracing and rescue operations
- **Modular Architecture**: Clean, maintainable code structure

## 📋 Requirements

- Raspberry Pi (3 or 4 recommended)
- Python 3.8 or higher
- Camera modules (for line tracing and rescue operations)
- Motor controllers with UART interface
- Ultrasonic sensors

## 🛠️ Installation

### Prerequisites

1. **Update your system:**
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

2. **Install system dependencies:**
   ```bash
   sudo apt install -y python3-pip python3-venv git
   ```

### Project Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/techno-robocup/robocup2025_raspberrypi_program.git
   cd robocup2025_raspberrypi_program
   ```

2. **Initialize and update submodules:**
   ```bash
   git submodule init
   git submodule update
   ```

3. **Create and activate virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Install the project:**
   ```bash
   pip install -e .
   ```

## 🔧 Configuration

### Environment Setup

The project uses `.envrc` for environment configuration. Make sure to:

1. **Enable direnv** (if using):
   ```bash
   direnv allow
   ```

2. **Configure camera settings** in `modules/settings.py`

3. **Set up UART communication** parameters

### Hardware Configuration

1. **Camera Setup:**
   - Connect cameras to specified ports
   - Configure camera parameters in settings

2. **Motor Controller:**
   - Connect via UART interface
   - Verify communication settings

3. **Ultrasonic Sensors:**
   - Connect sensors to appropriate pins
   - Test distance readings

## 🚀 Usage

### Running the Main Program

```bash
# Activate virtual environment
source venv/bin/activate

# Run the main program
python main.py
```

### Using the Console Script

```bash
# After installation, use the console script
robocup2025
```

### Development Scripts

- `fetch.sh`: Fetch latest submodule updates
- `send.sh`: Send data to external systems

## 📁 Project Structure

```
robocup2025_raspberrypi_program/
├── main.py                 # Main entry point
├── setup.py               # Package configuration
├── requirements.txt       # Python dependencies
├── modules/              # Submodule directory
│   └── [submodule content]
├── .github/              # GitHub workflows
├── .gitmodules           # Submodule configuration
├── fetch.sh              # Submodule update script
├── send.sh               # Data transmission script
└── test_installation.py  # Installation verification
```

## 🔌 Submodules

This project includes the following submodule:

### RoboCup 2025 Raspberry Pi Library

- **Path**: `modules/`
- **Repository**: https://github.com/techno-robocup/robocup2025_raspberrypi_library.git
- **Purpose**: Core robotics library with camera, UART, and sensor modules

### Managing Submodules

```bash
# Update submodules
git submodule update --remote

# Or use the provided script
./fetch.sh

# Initialize submodules (if not done)
git submodule init
git submodule update
```

## 🧪 Testing

Run the installation test to verify everything is working:

```bash
python test_installation.py
```

## 🔧 Development

### Code Style

The project uses:
- **YAPF** for code formatting (see `.style.yapf`)
- **Pylint** for code linting
- **Black** for additional formatting
- **Flake8** for style checking

### Running Tests

```bash
# Format code
yapf -i *.py modules/*.py

# Lint code
pylint *.py modules/*.py

# Style check
flake8 *.py modules/*.py
```

## 📝 API Reference

### Main Functions

- `send_speed(left_value, right_value)`: Send motor speed commands
- `get_ultrasonic_distance()`: Get ultrasonic sensor readings
- `send_wire_command(wire_number)`: Send wire commands for rescue operations

### Camera System

- `Rescue_Camera`: Camera for rescue operations
- `Linetrace_Camera`: Camera for line following

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For issues and questions:
- Check the [Issues](https://github.com/techno-robocup/robocup2025_raspberrypi_program/issues) page
- Review the submodule documentation in `modules/`
- Contact the RoboCup team

## 🏆 RoboCup 2025

This project is designed for the RoboCup 2025 competition. For competition-specific information and rules, please refer to the official RoboCup documentation.

---

**Note**: This is a robotics project requiring specific hardware. Make sure all hardware components are properly connected and configured before running the software.