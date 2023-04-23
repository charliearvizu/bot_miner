from pynput.keyboard import Listener, KeyCode

#listens for keyboard key presses
def on_press(key):
    global pressed_key
    try:
        pressed_key = key.char
    except:
          print(f'Error key pressed was:{key}\r\nEnter y/n')
    if key == KeyCode(char = 'y'):
            pressed_key = key.char
            return stop_keyboard_listener()
    elif key == KeyCode(char = 'n'):
         pressed_key = key.char
         return stop_keyboard_listener()
    else:
         print(f'Error key pressed was:{key}\r\nEnter y/n')

#stops the keyboard listener
def stop_keyboard_listener():
     return False

#returns the pressed key
def get_pressed_key():
    with Listener(on_press=on_press) as keybaord_listener:
        keybaord_listener.join()
    return pressed_key