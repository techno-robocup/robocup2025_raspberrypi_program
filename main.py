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
from enum import Enum
import traceback
import sys
import math
from typing import Optional
import time

logger = modules.log.get_logger()

logger.info("PROCESS STARTED")

# Rescue constants from modules.rescue
P = 0.5
WP = 0.5 # Cage P
AP = 1
CP = 1
BALL_CATCH_SIZE = 130000
CAGE_RELEASE_SIZE = 10000
TURN_45_TIME = 1
TURN_180_TIME = 4
FORWARD_STEP_TIME = 0.3
WALL_DIST_THRESHOLD = 5.03072
FRONT_CLEAR_THRESHOLD = 3.0
MOTOR_MIN = 1000
MOTOR_MAX = 2000
MOTOR_NEUTRAL = 1500

class ObjectClasses(Enum):
  BLACK_BALL = 0
  EXIT = 1
  GREEN_CAGE = 2
  RED_CAGE = 3
  SILVER_BALL = 4

# Rescue state variables
rescue_valid_classes = []
rescue_silver_ball_cnt = 0
rescue_black_ball_cnt = 0
rescue_is_ball_caching = False
rescue_target_position = None
rescue_target_size = None
rescue_cnt_turning_degrees = 0
rescue_cnt_turning_side = 0
rescue_L_Motor_Value = MOTOR_NEUTRAL
rescue_R_Motor_Value = MOTOR_NEUTRAL
rescue_Arm_Move_Flag = 0
rescue_L_U_SONIC = None
rescue_F_U_SONIC = None
rescue_R_U_SONIC = None

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
Linetrace_Camera.start_cam()

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
    uart_io.send_message(Message(message_id, f"Rescue {angle:4d}{wire}"))
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
is_object = False
object_second_phase = False


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
Is_Rescue_Camera_Start = False
Rescue_Camera.start_cam()


def main_loop():
  """Main control loop for the robotics program."""
  global message_id, is_object, object_second_phase, Is_Rescue_Camera_Start
  global rescue_valid_classes, rescue_silver_ball_cnt, rescue_black_ball_cnt
  global rescue_is_ball_caching, rescue_target_position, rescue_target_size
  global rescue_cnt_turning_degrees, rescue_cnt_turning_side
  global rescue_L_Motor_Value, rescue_R_Motor_Value, rescue_Arm_Move_Flag
  global rescue_L_U_SONIC, rescue_F_U_SONIC, rescue_R_U_SONIC
  message_id += 1

  try:
    # Check stop button first
    uart_io.send_message(Message(message_id, "GET button"))
    button_msg = uart_io.receive_message()
    if button_msg and button_msg.getMessage() != "ON":
      send_speed(1500, 1500)
      return

    distances = get_ultrasonic_distance()
    # if modules.settings.is_rescue_area:
    if False:
      if not Is_Rescue_Camera_Start:
        Rescue_Camera.start_cam()
        Linetrace_Camera.stop_cam()
        time.sleep(1)
        Is_Rescue_Camera_Start = True

      # Update ultrasonic values
      if distances and len(distances) >= 3:
        rescue_L_U_SONIC = distances[0]
        rescue_F_U_SONIC = distances[1]
        rescue_R_U_SONIC = distances[2]
        # Also update modules.rescue values for compatibility
        modules.rescue.L_U_SONIC = distances[0]
        modules.rescue.F_U_SONIC = distances[1]
        modules.rescue.R_U_SONIC = distances[2]
      else:
        logger.debug("No ultrasonic data available")

      # Check stop button before rescue logic
      uart_io.send_message(Message(message_id, "GET button"))
      button_msg = uart_io.receive_message()
      if button_msg and button_msg.getMessage() != "ON":
        send_speed(1500, 1500)
        return

      # EXPANDED RESCUE_LOOP_FUNC LOGIC
      if modules.settings.yolo_results is None:
        logger.debug("No YOLO results available, stopping motors.")
        # EXPANDED CHANGE_POSITION LOGIC
        send_speed(1750,1250)
        time.sleep(TURN_45_TIME)
        send_speed(1500,1500)
        rescue_cnt_turning_degrees += 45
        logger.debug(f"L: {rescue_L_Motor_Value} R: {rescue_R_Motor_Value}")
      else:
        results = modules.settings.yolo_results
        image_width = results[0].orig_shape[1]

        # Determine valid classes based on robot state
        if rescue_silver_ball_cnt == 2 and rescue_black_ball_cnt == 1:
          rescue_valid_classes = [ObjectClasses.EXIT.value]
        elif not rescue_is_ball_caching:
          rescue_valid_classes = [
              ObjectClasses.SILVER_BALL.value
          ] if rescue_silver_ball_cnt < 2 else [ObjectClasses.BLACK_BALL.value]
        else:
          rescue_valid_classes = [
              ObjectClasses.GREEN_CAGE.value
          ] if rescue_silver_ball_cnt < 2 else [ObjectClasses.RED_CAGE.value]

        # Update modules.rescue.Valid_Classes for compatibility
        modules.rescue.Valid_Classes = rescue_valid_classes

        # EXPANDED FIND_BEST_TARGET LOGIC
        boxes = results[0].boxes
        if not boxes:
          rescue_target_position = None
          rescue_target_size = None
        else:
          best_target_pos = None
          best_target_area = None
          min_dist = float("inf")
          cx = image_width / 2.0
          for box in boxes:
            try:
              cls = int(box.cls[0])
            except Exception:
              continue
            if cls in rescue_valid_classes:
              x_center, y_center, w, h = map(float, box.xywh[0])
              dist = x_center - cx
              area = w * h
              if abs(dist) < min_dist:
                min_dist = abs(dist)
                best_target_pos = dist
                best_target_area = area
              logger.debug(f"Detected cls={cls}, area={area:.1f}, offset={dist:.1f}")
          rescue_target_position = best_target_pos
          rescue_target_size = best_target_area
          if best_target_pos is not None:
            logger.debug(
                f"Target found offset={best_target_pos:.1f}, area={best_target_area:.1f}"
            )
          else:
            logger.debug("No valid target found")

        # Check stop button before motor control
        uart_io.send_message(Message(message_id, "GET button"))
        button_msg = uart_io.receive_message()
        if button_msg and button_msg.getMessage() != "ON":
          send_speed(1500, 1500)
          return

        if rescue_Arm_Move_Flag == 0:
          if rescue_target_position is None:
            logger.debug("No target found -> executing change_position()")
            # EXPANDED CHANGE_POSITION LOGIC
            logger.debug(f"SonicF :{rescue_F_U_SONIC} SonicL:{rescue_L_U_SONIC} cnt_turning:{rescue_cnt_turning_degrees}")
            rescue_L_Motor_Value = 1750
            rescue_R_Motor_Value = 1250
            time.sleep(TURN_45_TIME)
            rescue_L_Motor_Value = 1500
            rescue_R_Motor_Value = 1500
            rescue_cnt_turning_degrees += 45
            logger.debug(f"L: {rescue_L_Motor_Value} R: {rescue_R_Motor_Value}")
          else:
            rescue_cnt_turning_degrees = 0
            if not rescue_is_ball_caching and rescue_target_size >= BALL_CATCH_SIZE and abs(rescue_target_position) <= 100:
              logger.debug(
                  f"Target is close (size: {rescue_target_size:.1f}). Initiating catch_ball()"
              )
              # EXPANDED CATCH_BALL LOGIC
              logger.debug("Executing catch_ball()")
              rescue_is_ball_caching = True
              logger.debug("catch_ball done")
              rescue_Arm_Move_Flag = 1
              modules.rescue.Arm_Move_Flag = 1  # For compatibility
            elif rescue_is_ball_caching and rescue_F_U_SONIC is not None and rescue_F_U_SONIC < 10.0:
              logger.debug(
                  f"Close to wall (dist: {rescue_F_U_SONIC:.1f}). Initiating release_ball()")
              # EXPANDED RELEASE_BALL LOGIC
              logger.debug("Executing release_ball()")
              if rescue_valid_classes == [ObjectClasses.GREEN_CAGE.value]:
                rescue_silver_ball_cnt += 1
              else:
                rescue_black_ball_cnt += 1
              rescue_is_ball_caching = False  # Reset ball caching state
              rescue_Arm_Move_Flag = 2
              modules.rescue.Arm_Move_Flag = 2  # For compatibility
            else:
              logger.debug(
                  f"Targeting {rescue_valid_classes}, offset={rescue_target_position:.1f}. Navigating..."
              )
              # EXPANDED SET_MOTOR_SPEEDS LOGIC
              if rescue_target_position is None or rescue_target_size is None:
                rescue_L_Motor_Value = 1500
                rescue_R_Motor_Value = 1500
                logger.debug("No target data for set_motor_speeds(), stopping motors.")
              else:
                if not rescue_is_ball_caching:
                  diff_angle = rescue_target_position * P
                  if BALL_CATCH_SIZE > rescue_target_size:
                    dist_term = (math.sqrt(BALL_CATCH_SIZE) - math.sqrt(rescue_target_size)) * AP
                  else:
                    dist_term = 0
                    diff_angle * 2
                  base_L = 1500 + diff_angle + dist_term
                  base_R = 1500 - diff_angle + dist_term
                else:
                  diff_angle =rescue_target_position * WP
                  if CAGE_RELEASE_SIZE > rescue_target_size:
                    base_L = 1500 + diff_angle + 100
                    base_R = 1500 - diff_angle + 100
                  elif abs(rescue_target_position) <= 1000:
                    base_L = 1500 + diff_angle
                    base_R = 1500 - diff_angle
                  else:
                    base_L = 1500
                    base_R = 1500
                    rescue_Arm_Move_Flag = 2
                rescue_L_Motor_Value = int(min(max(base_L, 1000), 2000))
                rescue_R_Motor_Value = int(min(max(base_R, 1000), 2000))
        logger.debug(f"Motor Values after run: L={rescue_L_Motor_Value}, R={rescue_R_Motor_Value}, Sonic:{rescue_F_U_SONIC}")

      # Update modules.rescue values for compatibility
      modules.rescue.L_Motor_Value = rescue_L_Motor_Value
      modules.rescue.R_Motor_Value = rescue_R_Motor_Value
      modules.rescue.robot.silver_ball_cnt = rescue_silver_ball_cnt
      modules.rescue.robot.black_ball_cnt = rescue_black_ball_cnt
      modules.rescue.robot.is_ball_caching = rescue_is_ball_caching
      modules.rescue.robot.target_position = rescue_target_position
      modules.rescue.robot.target_size = rescue_target_size
      modules.rescue.robot.cnt_turning_degrees = rescue_cnt_turning_degrees
      modules.rescue.robot.cnt_turning_side = rescue_cnt_turning_side

      # Send motor speeds
      send_speed(rescue_L_Motor_Value, rescue_R_Motor_Value)

      # Handle arm movements
      if rescue_Arm_Move_Flag == 1:  # Ball catch
        logger.debug("Ball catch")
        send_speed(1500,1500)
        send_arm(1024,0)
        time.sleep(1)
        send_arm(1024,1)
        send_arm(3072,1)
        send_speed(1450,1450)
        time.sleep(1)
        send_speed(1500,1500)
        rescue_Arm_Move_Flag = 0
        modules.rescue.Arm_Move_Flag = 0
      if rescue_Arm_Move_Flag == 2:  # Ball release
        logger.debug("Ball release")
        send_speed(1600,1600)
        time.sleep(3)
        send_speed(1500,1500)
        send_arm(1024,1)
        time.sleep(1)
        send_arm(1024,0)
        send_arm(3072,0)
        send_speed(1450,1450)
        time.sleep(1)
        send_speed(1400,1400)
        time.sleep(3)
        send_speed(1750,1250)
        time.sleep(TURN_180_TIME)
        send_speed(1500,1500)
        rescue_Arm_Move_Flag = 0
        modules.rescue.Arm_Move_Flag = 0
    elif is_object:
      if not object_second_phase:
        send_speed(1750, 1250)
        time.sleep(1.5)
        send_speed(1700, 1700)
        time.sleep(1)
        object_second_phase = True
      else:
        if distances[0] < 8:
          send_speed(1700, 1700)
        else:
          send_speed(1580, 1720)
        if modules.settings.slope is not None and abs(modules.settings.slope) < 0.5:
          is_object = False
          object_second_phase = False
    #elif True:
    # send_arm(1024, 0)
    # time.sleep(3)
    # send_arm(3072, 0)
    # time.sleep(3)
    else:
      if Is_Rescue_Camera_Start:
        Rescue_Camera.stop_cam()
        Linetrace_Camera.start_cam()
        Is_Rescue_Camera_Start = False
      if modules.settings.stop_requested:
        send_speed(1500, 1500)
        logger.debug("Red stop")
        return
      if distances[1] < 8:
        is_object = True
        return
      if modules.settings.slope is None:
        send_speed(compute_default_speed() - 10, compute_default_speed() - 10)
        return

      current_theta = math.atan(modules.settings.slope)
      if current_theta < 0:
        current_theta += math.pi

      if current_theta > math.pi / 2:  # ← / に修正
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
        all_checks = [False, False]  # [left, right]
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
            time.sleep(3.5)
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
        is_object = False
        object_second_phase = False
        # Reset rescue state variables
        rescue_silver_ball_cnt = 0
        rescue_black_ball_cnt = 0
        rescue_is_ball_caching = False
        rescue_target_position = None
        rescue_target_size = None
        rescue_cnt_turning_degrees = 0
        rescue_cnt_turning_side = 0
        rescue_L_Motor_Value = MOTOR_NEUTRAL
        rescue_R_Motor_Value = MOTOR_NEUTRAL
        rescue_Arm_Move_Flag = 0

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
