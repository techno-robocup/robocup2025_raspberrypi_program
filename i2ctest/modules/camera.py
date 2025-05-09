from typing import Callable
from picamera2 import Picamera2


class Camera:

  def __init__(self, PORT: int, controls: dict[str, any], size: tuple[int, int],
               formats: str, lores_size: tuple[int, int],
               pre_callback_func: Callable[[any], any]):
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
    self.cam.start()

  def stop_cam(self):
    self.cam.stop()
