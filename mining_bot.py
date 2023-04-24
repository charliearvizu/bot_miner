import os
from dotenv import load_dotenv
from utils.mining_to_bank_util import multi_save_recording, replay, file_ore_box
from utils.inventory_checker_util import set_coords_for_screenshot, get_screenshot, check_change_screenshot_area
from utils.ore_mining_util import record_clicks
from utils.file_util import save_file_as_pkl_locally, save_screenshot, check_file_extension, load_pkl_file, load_screenshot, pick_random_file, file_deleter
from utils.keyboard_util import get_pressed_key
from utils.multiprocess_util import start_multiprocess

#loads the .env file
load_dotenv()

#sets virables to .env values 
sub_dir_moves = os.getenv('SUB_DIR_MOVES')
file_name_moves = os.getenv('FILE_NAME_MOVES')
sub_dir_png = os.getenv('SUB_DIR_PNG')
file_name_png = os.getenv('FILE_NAME_PNG')
sub_dir_ore = os.getenv('SUB_DIR_ORE')
file_name_ore = os.getenv('FILE_NAME_ORE')
file_name_fill_ore_box = os.getenv('FILE_NAME_FILL_ORE_BOX')
tolerance = int(os.getenv('TOLERANCE'))
click_offset = int(os.getenv('CLICK_OFFSET'))
wait_time = int(os.getenv('WAIT_TIME'))
mp_wait_time = int(os.getenv('MP_WAIT_TIME'))
replay_saves = int(os.getenv('REPLAY_SAVES'))

#initalizes the inventory checker
def initialize_inventory_checker():
    coords = set_coords_for_screenshot()
    save_file_as_pkl_locally(sub_dir_png, file_name_png, coords)
    initial_screenshot = get_screenshot(coords)
    save_screenshot(sub_dir_png, file_name_png, initial_screenshot)

#initializes ore clicker
def initialize_ore_clicker():
    ore_coords = record_clicks()
    save_file_as_pkl_locally(sub_dir_ore, file_name_ore, ore_coords)

#initializes the mining bot
def initialize_mining_bot():
    if check_file_extension(sub_dir_moves, '.pkl') == True:
        print('Replays found')
        print('Would you like to use current replays?(y/n)\r\n')
        key = get_pressed_key()
        if key == 'y':
            initialize_inventory_checker()
            initialize_ore_clicker()
            start_bot()
        elif key == 'n':
            file_deleter(sub_dir_moves)
            initialize_mining_bot()
    else:
        print('No replays found')
        multi_save_recording(sub_dir_moves, file_name_moves, replay_saves)
        print('Record you ore box filling clicks')
        file_ore_box(sub_dir_ore, file_name_fill_ore_box)
        initialize_mining_bot()


#starts the starts bot
def start_bot():
    load_inital_screenshot = load_screenshot(sub_dir_png, file_name_png)
    load_screenshot_coords = load_pkl_file(sub_dir_png, file_name_png)
    load_rock_corrds = load_pkl_file(sub_dir_ore, file_name_ore)
    load_fill_ore_replay = load_pkl_file(sub_dir_ore, file_name_fill_ore_box)
    is_inventory_full = False
    is_inventory_full = start_multiprocess(load_screenshot_coords, load_inital_screenshot, tolerance, load_rock_corrds, click_offset, wait_time, mp_wait_time)
    if is_inventory_full == True:
        replay(load_fill_ore_replay)
        is_inventory_full = check_change_screenshot_area(load_screenshot_coords, load_inital_screenshot, tolerance)
        if is_inventory_full == True:
            replay_file = load_pkl_file(sub_dir_moves, pick_random_file(sub_dir_moves))
            replay(replay_file)
            start_bot()
    print('Crashed')



#handles the multiprossing
if __name__ == '__main__':
    initialize_mining_bot()
