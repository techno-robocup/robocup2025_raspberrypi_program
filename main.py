"""
Main entry point for the RoboCup 2025 Raspberry Pi robotics program.

This module handles camera initialization, UART communication, and the main control loop
for line following and rescue operations.
"""

import modules.uart
import modules.log
import modules.camera
import modules.settings
import modules.rescue
from modules.uart import Message
import traceback
import sys
import math
from typing import Optional
import time

logger = modules.log.get_logger()

logger.info("PROCESS STARTED")

# Initialize camera objects
Rescue_Camera = modules.camera.Camera(
    PORT=modules.settings.RESCUE_CAMERA_PORT,
    controls=modules.settings.RESCUE_CAMERA_CONTROLS,
    size=modules.settings.RESCUE_CAMERA_SIZE,
    formats=modules.settings.RESCUE_CAMERA_FORMATS,
    lores_size=modules.settings.RESCUE_CAMERA_LORES_SIZE,
    pre_callback_func=modules.settings.RESCUE_CAMERA_PRE_CALLBACK_FUNC)

Linetrace_Camera = modules.camera.Camera(
    PORT=modules.settings.LINETRACE_CAMERA_PORT,
    controls=modules.settings.LINETRACE_CAMERA_CONTROLS,
    size=modules.settings.LINETRACE_CAMERA_SIZE,
    formats=modules.settings.LINETRACE_CAMERA_FORMATS,
    lores_size=modules.settings.LINETRACE_CAMERA_LORES_SIZE,
    pre_callback_func=modules.settings.LINETRACE_CAMERA_PRE_CALLBACK_FUNC)

# Initialize UART communication
uart_io = modules.uart.UART_CON()

# Start the line tracing camera
# Linetrace_Camera.start_cam()

message_id = 0


def send_speed(left_value: int, right_value: int) -> Message:
  """
    Send motor speed commands via UART.
    
    Args:
        left_value: Left motor speed value
        right_value: Right motor speed value
        
    Returns:
        Message: Message object if message sent successfully, None otherwise
    """
  global message_id
  message_id += 1
  try:
    uart_io.send_message(
        Message(message_id, f"MOTOR {int(left_value)} {int(right_value)}"))
    return uart_io.receive_message()
  except Exception as e:
    logger.error(f"Failed to send speed command: {e}")
    return None

def send_arm(angle: int, wire: int):
  global message_id
  message_id += 1
  try:
    uart_io.send_message(
      Message(message_id, f"Rescue {angle:4d}{wire}")
    )
    logger.debug(f"Sent Rescue {angle:4d}{wire}")
    logger.debug(f"Received message {uart_io.receive_message()}")
    return None
  except Exception as e:
    logger.error(f"Failed to send speed command: {e}")
    return None


def get_ultrasonic_distance() -> Optional[list[float]]:
  """
    Get ultrasonic sensor distance reading.
    
    Returns:
        Optional[list[float]]: List of distance readings or None if failed
    """
  try:
    logger.debug("Getting ultrasonic distance")
    global message_id
    message_id += 1
    uart_io.send_message(Message(message_id, "GET ultrasonic"))
    while True:
      response = uart_io.receive_message()
      if response and response.getId() == message_id:
        distances = response.getMessage().split()
        ret = []
        for distance in distances:
          try:
            ret.append(float(distance))
          except ValueError:
            logger.error(f"ValueError: Could not convert {distance} to float")
        return ret
      elif response.getId() > message_id:
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


def compute_moving_value(current_theta: float) -> float:
  """
    Compute motor movement value based on line slope.
    
    Args:
        current_theta: Current line slope
        
    Returns:
        float: Computed movement value
    """
  return modules.settings.COMPUTING_P * current_theta


default_speed = 1750


def compute_default_speed() -> int:
  """Compute default speed based on current slope."""
  global default_speed
  if modules.settings.slope is None:
    return default_speed

  current_theta = math.atan(modules.settings.slope)
  if current_theta < 0:
    current_theta += math.pi
  # Use absolute angle directly - larger angles = more turning = slower speed
  return int(default_speed - (abs(current_theta - math.pi / 2)**2) * 100)

# TODO: Removing some day
Rescue_Camera.start_cam()

def main_loop():
  """Main control loop for the robotics program."""
  global message_id
  message_id += 1

  try:
    if modules.settings.is_rescue_area:
      ##distances = get_ultrasonic_distance()
      ##if distances and len(distances) >= 3:
      #  #u_sonicL, u_sonicU, u_sonicR = distances[0], distances[1], distances[2]
      #modules.rescue.rescue_loop_func()
      ##else:
        #logger.debug("No ultrasonic data available")
      time.sleep(1)
      send_speed(modules.rescue.L_motor_value, modules.rescue.R_motor_value)
      send_arm(modules.rescue.Arm_pos, modules.rescue.Arm_pos)
      if modules.rescue.Release_flag:
        send_arm(3072, 0)
        time.sleep(3)
        send_arm(3072, 1)
        time.sleep(1)
        send_arm(3072, 0)
        send_arm(1024,0)
        time.sleep(3)
        modules.rescue.Release_flag = False
    #elif True:
    # send_arm(1024, 0)
    # time.sleep(3)
    # send_arm(3072, 0)
    # time.sleep(3)
    else:
      if modules.settings.stop_requested:
        send_speed(1500, 1500)
        time.sleep(5)
        logger.debug("Red stop")
        send_speed(1600, 1600)
        time.sleep(1)
        modules.settings.stop_requested = False
        return
      if modules.settings.slope is None:
        send_speed(compute_default_speed() - 10, compute_default_speed() - 10)
        return

      current_theta = math.atan(modules.settings.slope)
      if current_theta < 0:
        current_theta += math.pi

      if current_theta > math.pi / 2: # ← / に修正
        current_theta -= math.pi / 2
        send_speed(
            fix_to_range(
                compute_default_speed() - compute_moving_value(current_theta),
                1000, 2000),
            fix_to_range(
                compute_default_speed() + compute_moving_value(current_theta),
                1000, 2000))
      elif current_theta < math.pi / 2:
        current_theta = math.pi / 2 - current_theta
        send_speed(
            fix_to_range(
                compute_default_speed() + compute_moving_value(current_theta),
                1000, 2000),
            fix_to_range(
                compute_default_speed() - compute_moving_value(current_theta),
                1000, 2000))
      else:
        send_speed(compute_default_speed() - 10, compute_default_speed() - 10)

      if modules.settings.green_black_detected:
        all_checks = [False, False] # [left, right]
        should_detect = False
        for i in modules.settings.green_black_detected:
          if i[0] == 1:
            continue
          if i[1] == 0:
            continue
          if i[2] == 1:
            all_checks[0] = True
          if i[3] == 1:
            all_checks[1] = True
        for i in modules.settings.green_marks:
          if i[1] > modules.settings.LINETRACE_CAMERA_LORES_HEIGHT // 2:
            should_detect = True
            break
        if (all_checks[0] or all_checks[1]) and should_detect:
          send_speed(compute_default_speed(), compute_default_speed())
          time.sleep(0.5)
          if all_checks[0] and all_checks[1]:
            send_speed(1750, 1250)
            # time.sleep(5)
          elif all_checks[0]:
            send_speed(1750, 1250)
            time.sleep(1.5)
          elif all_checks[1]:
            send_speed(1200, 1750)
            time.sleep(1.5)


  except KeyboardInterrupt:
    logger.info("STOPPING PROCESS BY KeyboardInterrupt")
    send_speed(1500, 1500)
  except Exception as e:
    logger.error(f"Critical error: {str(e)}")
    logger.error(f"Error occurred at line {sys.exc_info()[2].tb_lineno}")
    logger.error(f"Traceback:\n{traceback.format_exc()}")


if __name__ == "__main__":
  try:
    while True:
      uart_io.send_message(Message(message_id, "GET button"))
      message = uart_io.receive_message()
      if message and message.getMessage() == "ON":
        main_loop()
      else:
        send_speed(1500, 1500)
        modules.settings.stop_requested = False
        modules.settings.is_rescue_area = False

  except KeyboardInterrupt:
    logger.info("PROCESS INTERRUPTED BY USER")
    send_speed(1500, 1500)
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
      send_speed(1500, 1500)
    except Exception as e:
      logger.error(f"Error during cleanup: {e}")
