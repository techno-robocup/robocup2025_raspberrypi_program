import modules.uart
import modules.log
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

if __name__ == "__main__":
  try:
    # Linetrace_Camera.start_cam()
    while True:
      pass
    # Linetrace_Camera.stop_cam()
  except KeyboardInterrupt:
    logger.debug("STOPPING PROCESS BY KeyboardInterrupt")
  except Exception as e:
    logger.error(f"An error occurred: {e}")
    logger.error(f"Traceback: {traceback.format_exc()}")
  finally:
    logger.debug("PROCESS ENDED")
    uart_io.close()
