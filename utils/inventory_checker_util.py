import numpy as np
import cv2
import mss
import time
from pynput import mouse

points = []

def get_screenshot(coords):
    with mss.mss() as sct:
        screenshot = np.array(sct.grab(coords))
    return cv2.cvtColor(screenshot, cv2.COLOR_RGB2GRAY)

def on_click(x, y, button, pressed):
    global points
    if pressed:
        points.append((x, y))
        return False
    if len(points) >= 2:
        return False
    
def set_coords_for_screenshot():
    print("Click the top left corner of the area you want to capture.")
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()
    top_left = points[0]
    print("Click the bottom right corner of the area you want to capture.")
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()
    bottom_right = points[1]
    coords = (*top_left, *bottom_right)
    return coords

def check_change_screenshot_area(coords, initial_screenshot, tolerance=10):
    screenshot = get_screenshot(coords)
    #initial_rezied = cv2.resize(initial_screenshot, (screenshot_gray.shape[1], screenshot_gray.shape[0]))
    diff = cv2.absdiff(initial_screenshot, screenshot)
    thresholded_diff = cv2.threshold(diff, tolerance, 255, cv2.THRESH_BINARY)[1]
    if cv2.countNonZero(thresholded_diff) > 0:
        print("Change detected!")
        change_detected = True
        return change_detected
        #Update the initial screenshot
        #initial_screenshot_gray = screenshot_gray
    else:
        print("No change detected.")
    # Wait for a short amount of time before taking the next screenshot

def mp_check_change_screenshot_area(event, coords, initial_screenshot, tolerance):
    while True:
        change = check_change_screenshot_area(coords, initial_screenshot, tolerance)
        time.sleep(45)
        if change == True:
            print('inventory is full')
            event.set()
            return False
        if event.is_set():
            return False
