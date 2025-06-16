import modules.uart
import modules.log
import modules.camera
from modules.uart import Message
import time
import traceback
import sys

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


def send_speed(l: int, r: int):
  uart_io.send_message(Message(0, f"MOTOR {l} {r}"))
  return


logger.info("OBJECTS INITIALIZED")

message_id = 0
if __name__ == "__main__":
  try:
    while True:
      logger.debug(f"SENDING TEST MESSAGE {message_id}")
      uart_io.send_message(Message(message_id, "TEST MESSAGE"))
      time.sleep(1)
      logger.debug(f"RECEIVING MESSAGE {message_id}")
      message = uart_io.receive_message()
      logger.debug(f"RECEIVED MESSAGE {message}")
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
