import modules.settings
import modules.camera

if __name__ == "__main__":
    Rescue_Camera = modules.camera.Camera(
        PORT=modules.settings.Rescue_Camera_PORT,
        controls=modules.settings.Rescue_Camera_Controls,
        size=modules.settings.Rescue_Camera_size,
        formats=modules.settings.Rescue_Camera_formats,
        lores_size=modules.settings.Rescue_Camera_lores_size,
        pre_callback_func=modules.settings.Rescue_Camera_Pre_Callback_func
    )

    try:
        Rescue_Camera.start_cam()

    finally:
        
        Rescue_Camera.stop_cam()
