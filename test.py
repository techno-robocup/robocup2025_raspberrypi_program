import modules.uart
import modules.log
import modules.settings
import modules.camera
from modules.uart import Message

logger = modules.log.get_logger()

logger.info("PROCESS STARTED")

# Rescue_Camera = modules.camera.Camera(
#     PORT=modules.settings.Rescue_Camera_PORT,
#     controls=modules.settings.Rescue_Camera_Controls,
#     size=modules.settings.Rescue_Camera_size,
#     formats=modules.settings.Rescue_Camera_formats,
#     lores_size=modules.settings.Rescue_Camera_lores_size,
#     pre_callback_func=modules.settings.Rescue_Camera_Pre_Callback_func)

# Linetrace_Camera = modules.camera.Camera(
#     PORT=modules.settings.Linetrace_Camera_PORT,
#     controls=modules.settings.Linetrace_Camera_Controls,
#     size=modules.settings.Linetrace_Camera_size,
#     formats=modules.settings.Linetrace_Camera_formats,
#     lores_size=modules.settings.Linetrace_Camera_lores_size,
#     pre_callback_func=modules.settings.Linetrace_Camera_Pre_Callback_func)

uart_io = modules.uart.UART_CON()
uart_io.init_connection()

logger.info("OBJECTS INITIALIZED")

message_id = 0
if __name__ == "__main__":
  try:
    modules.settings.Linetrace_Camera.start_cam()
    while True:
      logger.debug(f"SENDING TEST MESSAGE {message_id}")
      uart_io.send_message(Message(message_id, "TEST MESSAGE"))
      message_id += 1
      modules.settings.Linetrace_Camera.stop_cam()
  finally:
    logger.debug("PROCESS ENDED")
    uart_io.close()
