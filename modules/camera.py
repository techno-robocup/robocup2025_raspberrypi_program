from typing import Callable
from picamera2 import Picamera2
import modules.settings

class Camera:

    def __init__(self, PORT: int, controls: dict[str, any],
                 size: tuple[int, int], formats: str, lores_size: tuple[int,
                                                                        int],
                 pre_callback_func: Callable[[any], any]):
        """
      Initializes the Camera object with the specified configuration.

      Args:
          PORT (int): The port number for the camera.
          controls (dict[str, any]): A dictionary of camera control modules.settings.
          size (tuple[int, int]): The resolution size for the main camera configuration.
          formats (str): The format for the camera output.
          lores_size (tuple[int, int]): The resolution size for the low-resolution camera configuration.
          pre_callback_func (Callable[[any], any]): A callback function to be invoked before capturing.

      Configures the camera with the given settings and prepares it for preview and capture.
      """

        self.PORT = PORT
        self.controls = controls
        self.size = size
        self.format = formats
        self.lores_size = lores_size
        self.pre_callback_func = pre_callback_func
        self.cam = Picamera2(self.PORT)
        self.cam.preview_configuration.main.size = self.size
        self.cam.preview_configuration.main.format = self.format
        self.cam.configure(
            self.cam.create_preview_configuration(
                main={
                    "size": self.size,
                    "format": self.format
                },
                lores={
                    "size": self.lores_size,
                    "format": self.format
                },
            ))
        self.cam.pre_callback = self.pre_callback_func
        self.cam.set_controls(self.controls)

    def start_cam(self):

        """
        Starts the camera preview and capture process.

        This method initiates the camera operation using the pre-configured
        settings. It prepares the camera for capturing images or video
        based on the provided configuration during initialization.
        """

        self.cam.start()

    def stop_cam(self):

        """
        Stops the camera preview and capture process.

        This method is used to stop the camera after it has been started. It
        will stop the camera preview and capture process and release any
        system resources allocated during the camera operation.
        """
        self.cam.stop()


Rescue_Camera = Camera(
    PORT=modules.settings.Rescue_Camera_PORT,
    controls=modules.settings.Rescue_Camera_Controls,
    size=modules.settings.Rescue_Camera_size,
    formats=modules.settings.Rescue_Camera_formats,
    lores_size=modules.settings.Rescue_Camera_lores_size,
    pre_callback_func=modules.settings.Rescue_Camera_Pre_Callback_func)

Linetrace_Camera = Camera(
    PORT=modules.settings.Linetrace_Camera_PORT,
    controls=modules.settings.Linetrace_Camera_Controls,
    size=modules.settings.Linetrace_Camera_size,
    formats=modules.settings.Linetrace_Camera_formats,
    lores_size=modules.settings.Linetrace_Camera_lores_size,
    pre_callback_func=modules.settings.Linetrace_Camera_Pre_Callback_func)
