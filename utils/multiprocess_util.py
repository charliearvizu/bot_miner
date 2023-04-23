from utils.inventory_checker_util import mp_check_change_screenshot_area
from utils.ore_mining_util import mp_start_mining
import multiprocessing

#starts the mulitprocess event
def start_multiprocess(inital_screenshot_coords, inital_screenshot, tolerance, rock_corrds, click_offset, wait_time, mp_wait_time):
    
    event = multiprocessing.Event()
    p1 = multiprocessing.Process(target=mp_check_change_screenshot_area, args=(event, inital_screenshot_coords, inital_screenshot, tolerance, mp_wait_time))
    p2 = multiprocessing.Process(target=mp_start_mining, args=(event, rock_corrds, click_offset, wait_time))

    p1.start()
    p2.start()

    p1.join()
    p2.join()


