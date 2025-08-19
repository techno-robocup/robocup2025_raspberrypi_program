from libcamera import controls
from picamera2 import MappedArray
import cv2
import time
import numpy as np
import threading
import modules.log
import sys

logger = modules.log.get_logger()
DEBUG_MODE = True
Black_White_Threshold = 95

Linetrace_Camera_lores_height = 180
Linetrace_Camera_lores_width = 320
linetracecam_threadlock = threading.Lock()

# Line tracing variables
LASTBLACKLINE_LOCK = threading.Lock()
SLOPE_LOCK = threading.Lock()

lastblackline = Linetrace_Camera_lores_width // 2  # Initialize to center
slope = 0

computing_P = 500

# Green mark detection variables
min_green_area = 200  # Minimum area for a green mark to be considered valid
green_marks = []  # List to store all detected green marks
green_black_detected = [
]  # List to store black line detection around each green mark

min_red_area = 20  #TODO:Set red size
red_marks = []
red_black_detected = []

# Black line detection variables
min_black_line_area = 100  # Minimum area for a black line to be considered valid


def detect_green_marks(orig_image, blackline_image):
  """Detect multiple X-shaped green marks and their relationship with black lines."""
  image = orig_image.copy()
  global green_marks, green_black_detected

  # Convert to HSV
  hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

  # Define green color range
  # [h, s, v]
  lower_green = np.array([30, 0, 0])
  upper_green = np.array([110, 255, 255])

  # Create mask for green color
  green_mask = cv2.inRange(hsv, lower_green, upper_green)

  # Clean up noise
  kernel = np.ones((3, 3), np.uint8)
  green_mask = cv2.erode(green_mask, kernel, iterations=2)
  green_mask = cv2.dilate(green_mask, kernel, iterations=2)

  # Save green mask for debugging
  if DEBUG_MODE:
    cv2.imwrite(f"bin/{str(time.time())}_green_mask.jpg", green_mask)

  # Find contours
  contours, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL,
                                 cv2.CHAIN_APPROX_SIMPLE)

  # Reset global variables
  green_marks = []
  green_black_detected = []

  # Process each contour
  for contour in contours:
    if cv2.contourArea(contour) > min_green_area:
      # Get bounding box
      x, y, w, h = cv2.boundingRect(contour)
      logger.debug(f"Green mark found at ({x}, {y}) with size ({w}, {h})")

      # Calculate center point
      center_x = x + w // 2
      center_y = y + h // 2

      # Store mark info
      green_marks.append((center_x, center_y, w, h))

      # Check for black lines around the mark
      black_detections = np.zeros(4,
                                  dtype=np.int8)  # [bottom, top, left, right]

      # Define ROI sizes relative to mark size
      roi_width = int(w * 0.5)  # Half the width of the mark
      roi_height = int(h * 0.5)  # Half the height of the mark

      # Check bottom
      roi_b = blackline_image[center_y + h //
                              2:min(center_y + h // 2 +
                                    roi_height, Linetrace_Camera_lores_height),
                              center_x - roi_width // 2:center_x +
                              roi_width // 2]
      if roi_b.size > 0 and np.mean(roi_b) > Black_White_Threshold:
        black_detections[0] = 1

      # Check top
      roi_t = blackline_image[max(center_y - h // 2 -
                                  roi_height, 0):center_y - h // 2, center_x -
                              roi_width // 2:center_x + roi_width // 2]
      if roi_t.size > 0 and np.mean(roi_t) > Black_White_Threshold:
        black_detections[1] = 1

      # Check left
      roi_l = blackline_image[center_y - roi_height // 2:center_y +
                              roi_height // 2,
                              max(center_x - w // 2 -
                                  roi_width, 0):center_x - w // 2]
      if roi_l.size > 0 and np.mean(roi_l) > Black_White_Threshold:
        black_detections[2] = 1

      # Check right
      roi_r = blackline_image[center_y - roi_height // 2:center_y +
                              roi_height // 2, center_x + w //
                              2:min(center_x + w // 2 +
                                    roi_width, Linetrace_Camera_lores_width)]
      if roi_r.size > 0 and np.mean(roi_r) > Black_White_Threshold:
        black_detections[3] = 1

      green_black_detected.append(black_detections)

      if DEBUG_MODE:
        # Draw X mark
        cv2.line(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.line(image, (x + w, y), (x, y + h), (0, 255, 0), 2)
        # Draw center point
        cv2.circle(image, (center_x, center_y), 5, (0, 0, 255), -1)
        # Draw black line detection indicators
        if black_detections[0]:
          cv2.line(image, (center_x - 10, center_y + 10),
                   (center_x + 10, center_y + 10), (255, 0, 0), 2)
        if black_detections[1]:
          cv2.line(image, (center_x - 10, center_y - 10),
                   (center_x + 10, center_y - 10), (255, 0, 0), 2)
        if black_detections[2]:
          cv2.line(image, (center_x - 10, center_y - 10),
                   (center_x - 10, center_y + 10), (255, 0, 0), 2)
        if black_detections[3]:
          cv2.line(image, (center_x + 10, center_y - 10),
                   (center_x + 10, center_y + 10), (255, 0, 0), 2)

  # Save the image with X marks drawn on it
  if DEBUG_MODE and len(green_marks) > 0:
    cv2.imwrite(f"bin/{str(time.time())}_green_marks_with_x.jpg", image)


def detect_red_marks(orig_image, blackline_image):
  image = orig_image.copy()
  global red_marks, red_black_detected

  hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

  # lower_red1 = np.array([0, 40, 0])
  # upper_red1 = np.array([30, 255, 255])

  #TODO: Fix this range
  lower_red2 = np.array([190, 40, 0])
  upper_red2 = np.array([255, 255, 255])

  lower_red2 = np.array([130, 160, 0])
  upper_red2 = np.array([179, 255, 255])

  # red_mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
  red_mask = cv2.inRange(hsv, lower_red2, upper_red2)

  # Create overlapping mask using bitwise OR
  # red_mask = cv2.bitwise_or(red_mask1, red_mask2)

  # Clean up noise
  kernel = np.ones((3, 3), np.uint8)
  red_mask = cv2.erode(red_mask, kernel, iterations=2)
  red_mask = cv2.dilate(red_mask, kernel, iterations=2)

  if DEBUG_MODE:
    time_str = str(time.time())
    # cv2.imwrite(f"bin/{time_str}_red_mask1.jpg", red_mask1)
    # cv2.imwrite(f"bin/{time_str}_red_mask2.jpg", red_mask2)
    cv2.imwrite(f"bin/{time_str}_red_mask.jpg", red_mask)

  contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL,
                                 cv2.CHAIN_APPROX_SIMPLE)

  red_marks = []
  red_black_detected = []

  for contour in contours:
    logger.debug("In red contour check")
    if cv2.contourArea(contour) > min_red_area:
      logger.debug(f"Exitting {str(cv2.contourArea(contour))}")
      sys.exit(0)
      x, y, w, h = cv2.boundingRect(contour)

      center_x = x + w // 2
      center_y = y + h // 2
      red_marks.append((center_x, center_y, w, h))
      if center_y < image.shape[0] // 2:
        logger.debug("Read red line.")
        # sys.exit(0)  #TODO: Stop 3s
      # X mark & black line's border

      if DEBUG_MODE:
        # Draw X mark
        cv2.line(image, (x, y), (x + w, y + h), (0, 0, 255),
                 2)  # Red color for red marks
        cv2.line(image, (x + w, y), (x, y + h), (0, 0, 255), 2)
        # Draw center point
        cv2.circle(image, (center_x, center_y), 5, (0, 0, 255), -1)
        cv2.imwrite(f"bin/{time_str}_red_marks.jpg", image)
    else:
      logger.debug(f"Skipping because {str(cv2.contourArea(contour))}")


#@jit(nopython=True)
def Linetrace_Camera_Pre_callback(request):
  if DEBUG_MODE:
    logger.debug("Linetrace precallback called")

  # Global variables for line following
  global lastblackline, slope

  try:
    with linetracecam_threadlock:
      with MappedArray(request, "lores") as m:
        # Get image from camera
        image = m.array
        image2 = image.copy()

        # Get camera dimensions
        camera_x = Linetrace_Camera_lores_width
        camera_y = Linetrace_Camera_lores_height

        # Save original image for debugging
        if DEBUG_MODE:
          cv2.imwrite(f"bin/{str(time.time())}_original.jpg", image)

        # Convert image to grayscale
        gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

        # Create binary image with threshold for black line detection
        _, binary_image = cv2.threshold(gray_image, Black_White_Threshold, 255,
                                        cv2.THRESH_BINARY_INV)

        del gray_image

        # Save binary image for debugging
        if DEBUG_MODE:
          cv2.imwrite(f"bin/{str(time.time())}_binary.jpg", binary_image)

        # Clean up noise with morphological operations
        kernel = np.ones((3, 3), np.uint8)
        """
        1 1 1
        1 1 1
        1 1 1
        """
        binary_image = cv2.erode(binary_image, kernel, iterations=2)
        binary_image = cv2.dilate(binary_image, kernel, iterations=3)

        # Detect green marks and their relationship with black lines
        detect_red_marks(image2, binary_image)
        detect_green_marks(image, binary_image)

        # Find contours of the black line
        contours, _ = cv2.findContours(binary_image, cv2.RETR_TREE,
                                       cv2.CHAIN_APPROX_NONE)

        # If no contours found, keep previous values and return
        if not contours:
          slope = None
          return

        # Find the best contour to follow
        best_contour = find_best_contour(contours, camera_x, camera_y,
                                         lastblackline)

        if best_contour is None:
          slope = None
          return

        # Calculate center point of contour
        cx, cy = calculate_contour_center(best_contour)

        # Update global variables for line following
        with LASTBLACKLINE_LOCK:
          lastblackline = cx

        # Calculate slope for steering
        with SLOPE_LOCK:
          slope = calculate_slope(best_contour, cx, cy)

        # Create debug visualization if needed
        if DEBUG_MODE:
          debug_image = visualize_tracking(image, best_contour, cx, cy)
          cv2.imwrite(f"bin/{str(time.time())}_tracking.jpg", debug_image)

  except SystemExit:
    print("SystemExit caught")
    raise
  except Exception as e:
    if DEBUG_MODE:
      logger.error(f"Error in line tracing: {e}")


def find_best_contour(contours, camera_x, camera_y, last_center):
  """
  Find the best contour to follow from multiple candidates.
  Prioritizes contours at the bottom of the image and close to the last position.
  Also considers line width and continuity to handle intersections.
  
  Returns the selected contour or None if no suitable contour found.
  """
  # Initial candidate array structure: [contour_index, bottom_x1, bottom_y1, bottom_x2, bottom_y2, distance, width]
  candidates = np.array([[0, 0, 0, 0, 0, camera_x, 0]])
  bottom_contours = 0

  # Process each contour
  for i, contour in enumerate(contours):
    # Check minimum area requirement for black lines
    contour_area = cv2.contourArea(contour)
    if contour_area < min_black_line_area:
      if DEBUG_MODE:
        logger.debug(
            f"Black line contour {i} skipped: area {contour_area} < {min_black_line_area}"
        )
      continue  # Skip small contours

    # Get bounding box
    rect = cv2.minAreaRect(contour)
    box = cv2.boxPoints(rect)
    # Sort points by y-coordinate (descending)
    box = box[box[:, 1].argsort()[::-1]]

    # Calculate line width at bottom
    width = abs(box[0][0] - box[1][0])

    # Add to candidates
    candidates = np.append(candidates, [[
        i,
        int(box[0][0]),
        int(box[0][1]),
        int(box[1][0]),
        int(box[1][1]), camera_x, width
    ]],
                           axis=0)

    # Check if contour extends to bottom of image
    if box[0][1] >= (camera_y * 0.95):
      bottom_contours += 1

  # Remove initial placeholder row
  candidates = candidates[1:] if len(candidates) > 1 else None

  if candidates is None or len(candidates) == 0:
    return None

  # Sort candidates by y-coordinate (prioritize contours at bottom)
  candidates = candidates[candidates[:, 2].argsort()[::-1]]

  # If multiple contours at bottom, choose based on width and distance
  if bottom_contours > 1:
    for i in range(bottom_contours):
      con_num, x_cor1, y_cor1, x_cor2, y_cor2, _, width = candidates[i]
      # Calculate distance from last position
      center_x = (x_cor1 + x_cor2) / 2
      distance = abs(last_center - center_x)

      # Penalize very wide lines (likely intersections) unless they're very close to last position
      if width > 20 and distance > 30:  # Adjust these thresholds based on your needs
        distance *= 2

      candidates[i, 5] = distance

    # Sort bottom contours by distance from last position
    bottom_indices = list(range(bottom_contours))
    candidates[bottom_indices] = candidates[bottom_indices][
        candidates[bottom_indices][:, 5].argsort()]

  # Return best contour
  return contours[int(candidates[0][0])]


def calculate_contour_center(contour):
  """Calculate the center point of a contour."""
  M = cv2.moments(contour)
  if M["m00"] != 0:
    cx = int(M["m10"] / M["m00"])
    cy = int(M["m01"] / M["m00"])
  else:
    # Fallback to bounding box center
    x, y, w, h = cv2.boundingRect(contour)
    cx = x + w // 2
    cy = y + h // 2

  return cx, cy


def calculate_slope(contour, cx, cy):
  """Calculate the slope of the line for steering."""
  try:
    # Set base point
    base_x = Linetrace_Camera_lores_width // 2
    base_y = Linetrace_Camera_lores_height

    # Calculate slope between top and center points
    if cx != base_x:  # Avoid division by zero or tiny values
      return (base_y - cy) / (cx - base_x)
    else:
      return 10**9
  except Exception as e:
    if DEBUG_MODE:
      logger.error(f"Error in calculate_slope: {e}")
    return 0


def visualize_tracking(image, contour, cx, cy):
  """Create a visualization image showing tracking information."""
  # Make a copy of the image for drawing
  vis_image = image.copy()

  # Draw the contour
  cv2.drawContours(vis_image, [contour], 0, (0, 255, 0), 1)

  # Draw center point
  cv2.circle(vis_image, (cx, cy), 3, (0, 0, 255), -1)

  # Draw horizontal line at center of image
  h, w = vis_image.shape[:2]
  cv2.line(vis_image, (0, h // 2), (w, h // 2), (255, 0, 0), 1)

  # Draw vertical line at the tracked position
  cv2.line(vis_image, (cx, 0), (cx, h), (255, 0, 0), 1)

  return vis_image


def Rescue_Camera_Pre_callback(request):
  with MappedArray(request, "lores") as m:
    image = m.array
    cv2.imwrite(f"bin/{str(time.time())}_rescue.jpg", image)
    print("Rescue_Camera_Pre_callback")


Rescue_Camera_PORT = 0
Rescue_Camera_Controls = {
    "AfMode": controls.AfModeEnum.Continuous,
    "AfSpeed": controls.AfSpeedEnum.Fast,
    "AeFlickerMode": controls.AeFlickerModeEnum.Manual,
    "AeFlickerPeriod": 10000,
    "AeMeteringMode": controls.AeMeteringModeEnum.Matrix,
    "AwbEnable": True,
    "AwbMode": controls.AwbModeEnum.Indoor,
    "HdrMode": controls.HdrModeEnum.Off
}
Rescue_Camera_size = (4608, 2592)
Rescue_Camera_formats = "RGB888"
Rescue_Camera_lores_size = (Rescue_Camera_size[0] // 4,
                            Rescue_Camera_size[1] // 4)
Rescue_Camera_Pre_Callback_func = Rescue_Camera_Pre_callback

Linetrace_Camera_PORT = 1
Linetrace_Camera_Controls = {
    "AfMode": controls.AfModeEnum.Manual,
    "LensPosition": 1.0 / 0.03,
    "AeFlickerMode": controls.AeFlickerModeEnum.Manual,
    "AeFlickerPeriod": 10000,
    "AeMeteringMode": controls.AeMeteringModeEnum.Matrix,
    "AwbEnable": False,
    "AwbMode": controls.AwbModeEnum.Indoor,
    "HdrMode": controls.HdrModeEnum.Night
}
# Linetrace_Camera_size = (4608, 2592)
Linetrace_Camera_size = (3456, 2592)
Linetrace_Camera_formats = "RGB888"
Linetrace_Camera_lores_size = (Linetrace_Camera_lores_width,
                               Linetrace_Camera_lores_height)
Linetrace_Camera_Pre_Callback_func = Linetrace_Camera_Pre_callback


def timeout_function(func, args=(), kwargs={}, timeout=1):
  result = []
  error = []

  def target():
    try:
      result.append(func(*args, **kwargs))
    except Exception as e:
      error.append(e)

  thread = threading.Thread(target=target)
  thread.daemon = True
  thread.start()
  thread.join(timeout)

  if thread.is_alive():
    # Thread is still running, timeout occurred
    return None, TimeoutError(f"Function timed out after {timeout} seconds")
  if error:
    return None, error[0]
  return result[0] if result else None, None
