import pyautogui
import random
import time
from pynput.mouse import Listener


click_positions = []

def on_click(x, y, button, pressed):
    global click_positions
    if pressed:
        click_positions.append((x, y))
        return False
    if len(click_positions) >= 2:
        return False
    
def simulate_clicks(positions, click_offset, wait_time):
    for position in positions:
        click_x, click_y = position
        offset_x = click_x + random.randint(-click_offset, click_offset)
        offset_y = click_y + random.randint(-click_offset, click_offset)
        pyautogui.moveTo(offset_x, offset_y, duration=0.5, tween=pyautogui.easeInOutQuad)
        pyautogui.click()
        time.sleep(random.uniform(wait_time - 5, wait_time + 5))
        #print(f'click was orginially set at ({click_x},{click_y}) offset click is ({offset_x},{offset_y})')

def mp_simmulate_clicks(click_x, click_y, click_offset, wait_time):
        offset_x = click_x + random.randint(-click_offset, click_offset)
        offset_y = click_y + random.randint(-click_offset, click_offset)
        pyautogui.moveTo(offset_x, offset_y, duration=0.5, tween=pyautogui.easeInOutQuad)
        pyautogui.click()
        time.sleep(random.uniform(wait_time - 30, wait_time + 30))


def record_clicks():
    global click_positions
    click_positions = []
    print("Click the first position.")
    with Listener(on_click=on_click) as listener:
        listener.join()

    print("Click the second position.")
    with Listener(on_click=on_click) as listener:
        listener.join()

    return click_positions


def start_mining(click_offset, wait_time, positions):
    simulate_clicks(positions, click_offset, wait_time)


def mp_start_mining(event, coords, click_offset, wait_time):
    while not event.is_set():
        for position in coords:
            mp_simmulate_clicks(position[0], position[1], click_offset, wait_time)
            if event.is_set():
                break