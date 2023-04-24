import numpy as np
import cv2
import mss
import time
from pynput import mouse

#global list
points = []

#takes screenshot of specified screen coordinates
def get_screenshot(coords):
    with mss.mss() as sct:
        screenshot = np.array(sct.grab(coords))
    return cv2.cvtColor(screenshot, cv2.COLOR_RGB2GRAY)

#adds the first two click coordinates to the list
def on_click(x, y, button, pressed):
    global points
    if pressed:
        points.append((x, y))
        return False
    if len(points) >= 2:
        return False

#sets the top left and bottom right coordinates for screenshot capture   
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

#compares initial_creenshot to new screenshot taken at the given coords and compares the to for any changes
#defualt tolerance is set a 10 if not given one
def check_change_screenshot_area(coords, initial_screenshot, tolerance=10):
    screenshot = get_screenshot(coords)
    #initial_rezied = cv2.resize(initial_screenshot, (screenshot_gray.shape[1], screenshot_gray.shape[0]))
    diff = cv2.absdiff(initial_screenshot, screenshot)
    thresholded_diff = cv2.threshold(diff, tolerance, 255, cv2.THRESH_BINARY)[1]
    if cv2.countNonZero(thresholded_diff) > 0:
        change_detected = True
        return change_detected
        #Update the initial screenshot
        #initial_screenshot_gray = screenshot_gray
    else:
        print("No change detected.")
        return False

#multi process function that continuously calls check_change_screenshot_area
#if a True is returned by check_change_screenshot_area the multip process will exit
def mp_check_change_screenshot_area(event, coords, initial_screenshot, tolerance, mp_wait_time):
    while True:
        change = check_change_screenshot_area(coords, initial_screenshot, tolerance)
        if change == True:
            print('inventory is full')
            event.set()
            return False
        if event.is_set():
            return False
        time.sleep(mp_wait_time)
