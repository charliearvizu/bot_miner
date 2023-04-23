import pickle
import os
import shutil
import random
import cv2

#checks given sub dir if files with given extension exist
def check_file_extension(sub_dir, extensions):
    if not os.path.isdir(sub_dir):
        return False
    else:
        for file in os.listdir(sub_dir):
            if file.endswith(tuple(extensions)):
                return True

#deletes sub dir and files in the sub dir
def file_deleter(sub_dir):
    shutil.rmtree(sub_dir)
    print(f'dir:{sub_dir}/ has been deleted')


#returns a random file from a sub dir
def pick_random_file(sub_dir):
    file_list = os.listdir(sub_dir)
    file_names_no_ext = [os.path.splitext(file_name)[0] for file_name in file_list]
    random_list = random.randint(0, len(file_names_no_ext) - 1)
    return file_names_no_ext[random_list]


#creates sub dir with in working dir if it does not exist
def create_sub_dir(sub_dir):
    path = os.path.join(os.getcwd(), sub_dir)
    if not os.path.exists(path):
        os.makedirs(path)
    return(sub_dir)

#saves a data as pkl file 
def save_file_as_pkl_locally(sub_dir, file_name, data):
    path = create_sub_dir(sub_dir)
    with open(f'{os.path.join(path, file_name)}.pkl', 'wb') as f:
        pickle.dump(data, f)
    #print(f'Replay saved to \{path}\{file_name}.pkl')

#saves a screenshot locally
def save_screenshot(sub_dir, file_name, screenshot):
    cv2.imwrite(f'{os.path.join(create_sub_dir(sub_dir), file_name)}.png', screenshot)

#loads saved screenshot
def load_screenshot(sub_dir, file_name):
    img_path = os.path.join(sub_dir, file_name)
    img = cv2.imread(f'{img_path}.png', cv2.IMREAD_GRAYSCALE)
    return img

#loads saved pkl file
def load_pkl_file(sub_dir, file_name):
    file_location = os.path.join(sub_dir, f'{file_name}.pkl')
    with open(file_location, 'rb') as f:
        data = pickle.load(f)
    return data
