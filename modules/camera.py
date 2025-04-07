from typing import Callable
from picamera2 import Picamera2


class Camera:

    def __init__(self, PORT: int, controls: dict[str, any],
                 size: tuple[int, int], formats: str, lores_size: tuple[int,
                                                                        int],
                 pre_callback_func: Callable[[any], any]):
        """
    __init__ method of Camera class.
    
    Parameters
    ----------
    PORT : int
      The port number of the camera.
    controls : dict[str, any]
      The controls of the camera.
    size : tuple[int, int]
      The size of the camera.
    formats : str
      The format of the camera.
    lores_size : tuple[int, int]
      The size of the lores camera.
    pre_callback_func : Callable[[any], any]
      The callback function of the camera.
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
            cam.create_preview_configuration(
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
    Starts the camera for capturing video.

    This method starts the camera using the configuration set during initialization.
    """

        self.cam.start()

    def stop_cam(self):
        """
    Stops the camera.

    This method stops the camera from capturing video using the configuration set during initialization.
    """

        self.cam.stop()

from libcamera import controls

Rescue_Camera_Size = (4608, 2592)
Linetrace_Camera_Size = (4608, 2592)

def Rescue_Camera_Pre_callback(request):
  pass

def Linetrace_Camera_Pre_callback(request):
  pass

Rescue_Camera = Camera(
  PORT = 1,
  controls = { "AfMode": controls.AfModeEnum.Continuous, "AfSpeed": controls.AfSpeedEnum.Fast, "AeFlickerMode": controls.AeFlickerModeEnum.Manual, "AeFlickerPeriod": 10000, "AeMeteringMode": controls.AeMeteringModeEnum.Matrix, "AwbEnable": True, "AwbMode": controls.AwbModeEnum.Indoor, "HdrMode": controls.HdrModeEnum.Off },
  size = Rescue_Camera_Size,
  lores_size = (Rescue_Camera_Size[0]//4, Rescue_Camera_Size[1]//4),
  formats = "RGB888",
  pre_callback_func = Rescue_Camera_Pre_callback
)

Linetrace_Camera = Camera(
  PORT = 0,
  controls = { "AfMode": controls.AfModeEnum.Manual, "LensPosition": 1.0 / 0.03, "AeFlickerMode": controls.AeFlickerModeEnum.Manual, "AeFlickerPeriod": 10000, "AeMeteringMode": controls.AeMeteringModeEnum.Matrix, "AwbEnable": False, "AwbMode": controls.AwbModeEnum.Indoor, "HdrMode": controls.HdrModeEnum.Night },
  size = Linetrace_Camera_Size,
  lores_size = (Linetrace_Camera_Size[0]//4, Linetrace_Camera_Size[1]//4),
  formats = "RGB888",
  pre_callback_func = Linetrace_Camera_Pre_callback
)