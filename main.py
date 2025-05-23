import modules.i2cio
import modules.camera
import modules.settings
import serial

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
def serial_read():
    Serial_Port_id = "/dev/ttyUSB0"
    Serial_Port = serial.Serial(Serial_Port_id, 9600, timeout=3)
    while True:
        if Serial_Port !='':
            data = Serial_Port.readline()
            if data:  # Only process if we received data
                hex_data = ' '.join([f'{b:02X}' for b in data])
                print(f"Hex: {hex_data}")
if __name__ == "__main__":
  # Linetrace_Camera.start_cam()
  while True:
    serial_read()
  # Linetrace_Camera.stop_cam()
