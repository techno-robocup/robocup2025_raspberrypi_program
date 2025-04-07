from typing import Callable
from picamera2 import Picamera2
class Camera:
  def __init__(self, PORT: int, controls: dict[str, any], size: tuple[int, int], formats: str, lores_size: tuple[int, int], pre_callback_func: Callable[[any], any]):
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
    cam.preview_configuration.main.size = self.size
    cam.preview_configuration.main.format = self.format
    cam.configure(
      cam.create_preview_configuration(
        main={"size": self.size, "format": self.format},
        lores={"size": self.lores_size, "format": self.format},
      )
    )
    cam.pre_callback = self.pre_callback_func
    cam.set_controls(self.controls)
  def start_cam(self):
    """
    Starts the camera for capturing video.

    This method starts the camera using the configuration set during initialization.
    """

    cam.start()
  
  def stop_cam(self):
    """
    Stops the camera.

    This method stops the camera from capturing video using the configuration set during initialization.
    """

    cam.stop()