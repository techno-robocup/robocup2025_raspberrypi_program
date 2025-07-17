"""
Main entry point for the RoboCup 2025 Raspberry Pi robotics program.

This module handles camera initialization, UART communication, and the main control loop
for line following and rescue operations.
"""

import modules.uart
import modules.log
import modules.camera
from modules.uart import Message
import traceback
import sys
import math
import time
from typing import Optional

logger = modules.log.get_logger()

logger.info("PROCESS STARTED")

# Initialize camera objects
Rescue_Camera = modules.camera.Camera(
    PORT=modules.settings.Rescue_Camera_PORT,
    controls=modules.settings.Rescue_Camera_Controls,
    size=modules.settings.Rescue_Camera_size,
    formats=modules.settings.Rescue_Camera_formats,
    lores_size=modules.settings.Rescue_Camera_lores_size,
    pre_callback_func=modules.settings.Rescue_Camera_Pre_Callback_func)

Linetrace_Camera = modules.camera.Camera(
    PORT=modules.settings.Linetrace_Camera_PORT,
    controls=modules.settings.Linetrace_Camera_Controls,
    size=modules.settings.Linetrace_Camera_size,
    formats=modules.settings.Linetrace_Camera_formats,
    lores_size=modules.settings.Linetrace_Camera_lores_size,
    pre_callback_func=modules.settings.Linetrace_Camera_Pre_Callback_func)

# Initialize UART communication
uart_io = modules.uart.UART_CON()

# Start the line tracing camera
Linetrace_Camera.start_cam()

message_id = 0


def send_speed(left_value: int, right_value: int) -> bool:
  """
    Send motor speed commands via UART.
    
    Args:
        left_value: Left motor speed value
        right_value: Right motor speed value
        
    Returns:
        bool: True if message sent successfully, False otherwise
    """
  global message_id
  message_id += 1
  try:
    uart_io.send_message(
        Message(message_id, f"MOTOR {int(left_value)} {int(right_value)}"))
    return True
  except Exception as e:
    logger.error(f"Failed to send speed command: {e}")
    return False


def get_ultrasonic_distance() -> Optional[float]:
  """
    Get ultrasonic sensor distance reading.
    
    Returns:
        Optional[float]: Distance reading or None if failed
    """
  try:
    global message_id
    message_id += 1
    while True:
      uart_io.send_message(Message(message_id, "GET ultrasonic"))
      response = uart_io.receive_message()
      if response and response.getId() == message_id:
        return float(response.getMessage())
      elif not response:
        break
    return None
  except Exception as e:
    logger.error(f"Failed to get ultrasonic distance: {e}")
    return None


def send_wire_command(wire_number: int) -> Message:
  """
    Send wire command via UART.
    
    Args:
        wire_number: Wire number to send
        
    Returns:
        Message: Message object if message sent successfully, None otherwise
  """
  global message_id
  message_id += 1
  try:
    uart_io.send_message(Message(message_id, f"Wire {wire_number}"))
    while True:
      response = uart_io.receive_message()
      if response and response.getId() == message_id:
        return response
      elif not response:
        break
    return None
  except Exception as e:
    logger.error(f"Failed to send wire command: {e}")
    return None


logger.info("OBJECTS INITIALIZED")


def fix_to_range(x: int, min_num: int, max_num: int) -> int:
  """
    Clamp a value to a specified range.
    
    Args:
        x: Value to clamp
        min_num: Minimum allowed value
        max_num: Maximum allowed value
        
    Returns:
        int: Clamped value
    """
  return max(min_num, min(x, max_num))


def compute_moving_value(current_slope: int) -> float:
  """
    Compute motor movement value based on line slope.
    
    Args:
        current_slope: Current line slope
        
    Returns:
        float: Computed movement value
    """
  if current_slope == 0:
    return 0.0
  return modules.settings.computing_P * math.sqrt(1 / abs(current_slope))


def main_loop():
  """Main control loop for the robotics program."""
  global message_id

  try:
    while True:
      # TODO: Uncomment when button functionality is implemented
      # uart_io.send_message(Message(message_id, "GET button"))
      # message = uart_io.receive_message()

      # Temporary hardcoded button state for testing
      message = Message(1, "ON")

      if message and message.getMessage() == "OFF":
        logger.debug("BUTTON OFF")
      else:
        logger.debug("BUTTON ON")

        # Test wire commands
        response = send_wire_command(0)
        if response:
          print("MESSAGE: ", response.getMessage())
        time.sleep(1)

        response = send_wire_command(1)
        if response:
          print("MESSAGE: ", response.getMessage())
        time.sleep(1)

      message_id += 1

  except KeyboardInterrupt:
    logger.info("STOPPING PROCESS BY KeyboardInterrupt")
  except Exception as e:
    logger.error(f"Critical error: {str(e)}")
    logger.error(f"Error occurred at line {sys.exc_info()[2].tb_lineno}")
    logger.error(f"Traceback:\n{traceback.format_exc()}")


if __name__ == "__main__":
  try:
    main_loop()
  except KeyboardInterrupt:
    logger.info("PROCESS INTERRUPTED BY USER")
  except Exception as e:
    logger.error(f"Fatal error: {str(e)}")
    logger.error(f"Traceback:\n{traceback.format_exc()}")
  finally:
    # Cleanup
    try:
      uart_io.close()
      Linetrace_Camera.stop_cam()
      Rescue_Camera.stop_cam()
      logger.info("PROCESS ENDED")
    except Exception as e:
      logger.error(f"Error during cleanup: {e}")
