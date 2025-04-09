import time
import random
from modules.i2cio import i2cio
from modules.camera import Rescue_Camera, Linetrace_Camera
from time import sleep

if __name__ == "__main__":
    Linetrace_Camera.start_cam()
    sleep(1)
    Linetrace_Camera.stop_cam()
