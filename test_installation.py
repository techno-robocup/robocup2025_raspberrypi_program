#!/usr/bin/env python3
"""
Test script for RoboCup 2025 Raspberry Pi program.

This script tests all major components to ensure they're working correctly.
"""

import sys
from typing import List, Tuple


def test_imports() -> Tuple[bool, List[str]]:
  """Test if all required modules can be imported."""
  errors = []
  success = True

  modules_to_test = [
      "modules.uart", "modules.log", "modules.camera", "modules.settings",
      "cv2", "numpy", "serial", "threading", "time"
  ]

  print("Testing module imports...")
  for module in modules_to_test:
    try:
      __import__(module)
      print(f"✓ {module}")
    except ImportError as e:
      print(f"✗ {module}: {e}")
      errors.append(f"{module}: {e}")
      success = False

  return success, errors


def test_logging() -> Tuple[bool, List[str]]:
  """Test logging functionality."""
  errors = []
  success = True

  try:
    import modules.log
    logger = modules.log.get_logger("test")
    logger.info("Test log message")
    print("✓ Logging system")
  except Exception as e:
    print(f"✗ Logging: {e}")
    errors.append(f"Logging: {e}")
    success = False

  return success, errors


def test_message_class() -> Tuple[bool, List[str]]:
  """Test Message class functionality."""
  errors = []
  success = True

  try:
    from modules.uart import Message

    # Test constructor with id and message
    msg1 = Message(1, "TEST")
    assert msg1.getId() == 1
    assert msg1.getMessage() == "TEST"

    # Test constructor with combined string
    msg2 = Message("2 TEST2")
    assert msg2.getId() == 2
    assert msg2.getMessage() == "TEST2"

    print("✓ Message class")
  except Exception as e:
    print(f"✗ Message class: {e}")
    errors.append(f"Message class: {e}")
    success = False

  return success, errors


def test_camera_config() -> Tuple[bool, List[str]]:
  """Test camera configuration."""
  errors = []
  success = True

  try:
    import modules.settings

    # Test that camera configurations exist
    assert hasattr(modules.settings, 'Linetrace_Camera_PORT')
    assert hasattr(modules.settings, 'Rescue_Camera_PORT')
    assert hasattr(modules.settings, 'Linetrace_Camera_Controls')
    assert hasattr(modules.settings, 'Rescue_Camera_Controls')

    print("✓ Camera configuration")
  except Exception as e:
    print(f"✗ Camera configuration: {e}")
    errors.append(f"Camera configuration: {e}")
    success = False

  return success, errors


def test_algorithm_functions() -> Tuple[bool, List[str]]:
  """Test algorithm functions."""
  errors = []
  success = True

  try:

    # Test fix_to_range function
    from main import fix_to_range
    assert fix_to_range(5, 0, 10) == 5
    assert fix_to_range(-1, 0, 10) == 0
    assert fix_to_range(15, 0, 10) == 10

    # Test compute_moving_value function
    from main import compute_moving_value
    result = compute_moving_value(1)
    assert isinstance(result, (int, float))

    print("✓ Algorithm functions")
  except Exception as e:
    print(f"✗ Algorithm functions: {e}")
    errors.append(f"Algorithm functions: {e}")
    success = False

  return success, errors


def main():
  """Run all tests."""
  print("=== RoboCup 2025 Installation Test ===\n")

  tests = [
      ("Module Imports", test_imports),
      ("Logging System", test_logging),
      ("Message Class", test_message_class),
      ("Camera Configuration", test_camera_config),
      ("Algorithm Functions", test_algorithm_functions),
  ]

  all_success = True
  all_errors = []

  for test_name, test_func in tests:
    print(f"\n--- {test_name} ---")
    success, errors = test_func()
    all_success = all_success and success
    all_errors.extend(errors)

  print("\n=== Test Results ===")
  if all_success:
    print("✓ All tests passed!")
    print("\nInstallation is complete and ready to use.")
    print("You can now run: python3 main.py")
  else:
    print("✗ Some tests failed:")
    for error in all_errors:
      print(f"  - {error}")
    print("\nPlease check the error messages above and fix any issues.")
    sys.exit(1)


if __name__ == "__main__":
  main()
