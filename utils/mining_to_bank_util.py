from pynput.mouse import Listener, Button, Controller
from utils.file_util import save_file_as_pkl_locally
import time

#global vars
events = []
is_recording = False

#listens for a mouse left or middle click
#records postion of left clicks
#stops the listener on middle clicks
def on_click(x, y, button, pressed):
    global is_recording, events
    if pressed:
        is_recording = True
        if button == Button.left:
            print('Recording in progress....')
            events.append(('click', x, y, time.time()))
        elif button == Button.middle:
            is_recording = False
            print('Stopped Recording')
            return False

#appends the time and postion traveled between left clicks
def on_move(x, y):
    global is_recording, events
    if is_recording:
        events.append(('move', x, y, time.time()))

#starts the listener
def start_recording():
    with Listener(on_click=on_click, on_move=on_move) as listener:
        print('Left click to start recording')
        print('Click scroll wheel to stop recording')
        listener.join()

#will keep and save given number of replays
def multi_save_recording(sub_dir, file_name, number_replays):
    global is_recording, events
    for i in range(number_replays):
        if i <= number_replays:
            file_name_num = f'{file_name}_{i}'
            start_recording()
            save_file_as_pkl_locally(sub_dir, file_name_num, events)
            del events[:]

#replays the save save left mouse clicks   
def replay(replay_data):
    mouse = Controller()
    prev_time = None
    for event in replay_data:
        if event[0] == 'click':
            if prev_time is None:
                prev_time = event[3]
            else:
                time_diff = (event[3] - prev_time)
                time.sleep(time_diff)
                prev_time = event[3]
            mouse.position = (event[1], event[2])
            mouse.click(Button.left)
        elif event[0] == 'right_click':
            if prev_time is None:
                prev_time = event[3]
            else:
                time_diff = (event[3] - prev_time)
                time.sleep(time_diff)
                prev_time = event[3]
            mouse.position = (event[1], event[2])
            mouse.click(Button.right)
        elif event[0] == 'move':
            if prev_time is None:
                prev_time = event[3]
            else:
                time_diff = (event[3] - prev_time)
                time.sleep(time_diff)
                prev_time = event[3]
            mouse.position = (event[1], event[2])
