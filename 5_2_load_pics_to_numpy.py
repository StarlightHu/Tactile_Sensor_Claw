import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from datetime import datetime
import cv2

# import torch
# import torchvision.models
# from torchvision import transforms

#########test

from load_labels_to_memomery import load_labels_to_memomery

LABEL_PATH = "/Volumes/USB128/lab_data"
DATA_PATH = "/Volumes/USB128/train_pic/3"
CACHE_PATH = "/Volumes/USB128/tmp"





test_dict = load_labels_to_memomery(LABEL_PATH, True)

####### test ###########


def load_pics_and_labels_to_numpy(datas_path, labels_dict, cache_path, pickup=100):
    if not os.path.exists(datas_path):
        raise Exception("Datas path does not exist.")

    datas_list = []
    labels_list = []

    notice_time = 5  # 控制打印进度的
    len_DIR = len(os.listdir(os.path.join(datas_path)))
    load_cnt = 0
    gen_cnt = 0
    start_time = datetime.now()
    print("Start at {}.".format(start_time.strftime('%Y_%m_%d_%H_%M_%S_%f')))
    pre_pro = None
    for process, DIR in enumerate(os.listdir(os.path.join(datas_path))):
        if DIR[0] == ".":  # 跳过隐藏文件
            continue

        SET, LABEL = get_info_set_and_label(os.path.join(datas_path, DIR))
        # str, int SET = 1, 2, 3, 4... LABEL = 1, 2, 3, 4...
        if labels_dict[SET][LABEL - 1] is None:
            continue

        if have_cached(cache_path, DIR):
            three_data_np = load_numpy_cache(cache_path, DIR)
            load_cnt += 1
        else:
            three_data_list = []    # 每份data是6个, 这个最后会有18份

            for i in range(3):
                for j in range(6):
                    video_name = str(i)
                    pic_name = str(j).zfill(10) + ".jpg"
                    three_data_list.append(single_img_to_numpy(os.path.join(
                        datas_path,
                        DIR,
                        video_name,
                        pic_name)))

            three_data_cache_np = np.array(three_data_list)   # shape (18, 244, 224, 3)
            # np.save("val_x.npy", val_x)
            # three_data_cache_np = three_data_cache_np.reshape((18, -1), order="C")
            store_numpy_cache(cache_path, DIR, three_data_cache_np)
            three_data_np = load_numpy_cache(cache_path, DIR)

            gen_cnt += 1

        single_label_np = np.array([labels_dict[SET][LABEL - 1]])

        # three_data_np = three_data_np.reshape((18, 244, 224, 3), order="C")

        for i in range(3):
            datas_list.append(three_data_np[i*6:(i+1)*6, ])
            labels_list.append(single_label_np)

        #  太耗时, 打印进度
        process_in_per = int((process + 1) * 100 / len_DIR)
        if process_in_per != 0 and process_in_per % notice_time == 0:
            if pre_pro != process_in_per:
                print("{0}%; load: {1} / {3}; generate: {2} / {3}; {4}".format(
                    process_in_per,
                    load_cnt,
                    gen_cnt,
                    len_DIR,
                    (datetime.now() - start_time).total_seconds()
                ))
                pre_pro = process_in_per

        if process / len_DIR > pickup / 100:
            # 由于不想改数据加载乐, 所以直接抛弃一些数据好了
            break

    print("Loading is done.")

    return np.array(datas_list), np.array(labels_list)


def single_img_to_numpy(img_path):
    img = cv2.imread(img_path)
    img = cv2.resize(img, (224, 244))
    img = img.astype(np.float32) / 255.
    return img


def get_info_set_and_label(DIR_path):
    fl = open(os.path.join(DIR_path, "info.txt"))

    content = fl.readline()
    set_num = int(content.split("\n")[0].split(":")[-1])

    fl.readline()  # 空读

    content = fl.readline()
    label_num = int(content.split("\n")[0].split(":")[-1])

    fl.close()

    return str(set_num), label_num


def have_cached(cache_path, DIR):
    return os.path.exists(os.path.join(cache_path, DIR + ".npy"))


def store_numpy_cache(cache_path, DIR, np_array):
    npy_path = os.path.join(cache_path, DIR + ".npy")
    np.save(npy_path, np_array)


def load_numpy_cache(cache_path, DIR):
    npy_path = os.path.join(cache_path, DIR + ".npy")
    return np.load(npy_path)


if __name__ == '__main__':
    a, b = load_pics_and_labels_to_numpy(DATA_PATH, test_dict, CACHE_PATH)
    pass
