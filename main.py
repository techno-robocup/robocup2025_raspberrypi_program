import modules.uart
import modules.log
logger = modules.log.get_logger()

logger.info("PROGRAM START")



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


if __name__ == "__main__":
  logger.debug("PROCESS STARTED")
  uart_io = modules.uart.UART_CON()
  uart_io.init_connection()
  # Linetrace_Camera.start_cam()
  while True:
    pass
  # Linetrace_Camera.stop_cam()
