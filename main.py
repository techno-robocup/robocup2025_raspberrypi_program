import modules.uart
import modules.log
import modules.camera
from modules.uart import Message
import traceback
import sys
import math
import time

logger = modules.log.get_logger()

logger.info("PROCESS STARTED")

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

uart_io = modules.uart.UART_CON()

Linetrace_Camera.start_cam()

message_id = 0


def send_speed(left_value: int, right_value: int):
  uart_io.send_message(
      Message(message_id, f"MOTOR {int(left_value)} {int(right_value)}"))
  return


def get_ultrasonic_distance():
  uart_io.send_message(Message(message_id, "GET ultrasonic"))
  return


logger.info("OBJECTS INITIALIZED")


def fix_to_range(x: int, min_num: int, max_num: int):
  return max(min_num, min(x, max_num))


def compute_moving_value(current_slope: int):
  return modules.settings.computing_P * math.sqrt(1 / current_slope)


if __name__ == "__main__":
  try:
    while True:
      # uart_io.send_message(Message(message_id, "GET button"))
      # message = uart_io.receive_message()
      message = Message(1, "ON")
      if message != False and message.getMessage() == "OFF":
        logger.debug("BUTTON OFF")
      else:
        logger.debug("BUTTON ON")
        send_speed(1600, 1600)
      message_id += 1
  except KeyboardInterrupt:
    logger.info(
        f"STOPPING PROCESS BY KeyboardInterrupt at line {sys.exc_info()[2].tb_lineno}"
    )
    logger.info(f"Traceback:\n{traceback.format_exc()}")
  except Exception as e:
    logger.error(f"Critical error: {str(e)}")
    logger.error(f"Error occurred at line {sys.exc_info()[2].tb_lineno}")
    logger.error(f"Traceback:\n{traceback.format_exc()}")
  finally:
    uart_io.close()
    Linetrace_Camera.stop_cam()
    logger.info("PROCESS ENDED")
