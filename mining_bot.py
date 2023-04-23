import os
import sys
from dotenv import load_dotenv
from utils.mining_to_bank_util import multi_save_recording, replay
from utils.inventory_checker_util import set_coords_for_screenshot, get_screenshot
from utils.ore_mining_util import record_clicks
from utils.file_util import save_file_as_pkl_locally, save_screenshot, check_file_extension, load_pkl_file, load_screenshot, pick_random_file, file_deleter
from utils.keyboard_util import get_pressed_key
from utils.multiprocess_util import start_multiprocess

load_dotenv()

sub_dir_moves = os.getenv('SUB_DIR_MOVES')
file_name_moves = os.getenv('FILE_NAME_MOVES')
sub_dir_png = os.getenv('SUB_DIR_PNG')
file_name_png = os.getenv('FILE_NAME_PNG')
sub_dir_rock = os.getenv('SUB_DIR_ROCK')
file_name_rock = os.getenv('FILE_NAME_ROCKS')
tolerance = int(os.getenv('TOLERANCE'))
click_offset = int(os.getenv('CLICK_OFFSET'))
wait_time = int(os.getenv('WAIT_TIME'))
replay_saves = int(os.getenv('REPLAY_SAVES'))

def initialize_inventory_checker():
    coords = set_coords_for_screenshot()
    save_file_as_pkl_locally(sub_dir_png, file_name_png, coords)
    initial_screenshot = get_screenshot(coords)
    save_screenshot(sub_dir_png, file_name_png, initial_screenshot)


def initialize_rock_clicker():
    rock_coords = record_clicks()
    save_file_as_pkl_locally(sub_dir_rock, file_name_rock, rock_coords)

def initialize_mining_bot():
    if check_file_extension(sub_dir_moves, '.pkl') == True:
        print('Replays found')
        print('Would you like to use current replays?(y/n)\r\n')
        key = get_pressed_key()
        if key == 'y':
            initialize_inventory_checker()
            initialize_rock_clicker()
            start_bot()
        elif key == 'n':
            file_deleter(sub_dir_moves)
            initialize_mining_bot()
    else:
        print('No replays found')
        multi_save_recording(sub_dir_moves, file_name_moves, replay_saves)
        initialize_mining_bot()



def start_bot():
    load_inital_screenshot = load_screenshot(sub_dir_png, file_name_png)
    load_screenshot_coords = load_pkl_file(sub_dir_png, file_name_png)
    load_rock_corrds = load_pkl_file(sub_dir_rock, file_name_rock)
    start_multiprocess(load_screenshot_coords, load_inital_screenshot, tolerance, load_rock_corrds, click_offset, wait_time)
    replay_file = load_pkl_file(sub_dir_moves, pick_random_file(sub_dir_moves))
    replay(replay_file)
    start_bot()



if __name__ == '__main__':
    initialize_mining_bot()
