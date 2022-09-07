import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from datetime import datetime

# import torch
# import torchvision.models
# from torchvision import transforms

#########test

from load_labels_to_memomery import load_labels_to_memomery

LABEL_PATH = "/Volumes/USB128/lab_data"
DATA_PATH = "/Volumes/USB128/train_pic/3"
CACHE_PATH = "/Volumes/USB128/tmp"


def single_img_to_numpy2(img_path):
    if not os.path.exists(img_path):
        print(img_path)
        print("Oh shit")
        exit(0)
    return np.zeros((1000,))


test_dict = load_labels_to_memomery(LABEL_PATH, True)


# TESt


def load_pics_and_labels_to_numpy(datas_path, labels_dict, cache_path):
    if not os.path.exists(datas_path):
        raise Exception("Datas path does not exist.")

    datas_list = []
    labels_list = []

    notice_time = 5  # 控制打印进度的
    len_DIR = len(os.listdir(os.path.join(datas_path)))
    load_cnt = 0
    gen_cnt = 0
    start_time = datetime.now()
    for process, DIR in enumerate(os.listdir(os.path.join(datas_path))):
        if DIR[0] == ".":  # 跳过隐藏文件
            continue

        SET, LABEL = get_info_set_and_label(os.path.join(datas_path, DIR))
        # str, int SET = 1, 2, 3, 4... LABEL = 1, 2, 3, 4...
        if labels_dict[SET][LABEL - 1] is None:
            continue

        if have_cached(cache_path, DIR):
            single_data_np = load_numpy_cache(cache_path, DIR)
            load_cnt += 1
        else:
            single_data_list = []

            for i in range(3):
                for j in range(6):
                    video_name = str(i)
                    pic_name = str(j).zfill(10) + ".jpg"
                    single_data_list.append(single_img_to_numpy(os.path.join(
                        datas_path,
                        DIR,
                        video_name,
                        pic_name)))

            single_data_cache_np = np.array(single_data_list)
            store_numpy_cache(cache_path, DIR, single_data_cache_np)
            single_data_np = load_numpy_cache(cache_path, DIR)

            gen_cnt += 1



        single_label_np = np.array([labels_dict[SET][LABEL - 1]
                                    for _ in range(6)])

        datas_list.append(single_data_np)
        labels_list.append(single_label_np)



        #  太耗时, 打印进度
        process_in_per = int((process + 1) * 100 / len_DIR)
        if process_in_per != 0 and process_in_per % notice_time == 0:
            print("{0}%; load: {1} / {3}; generate: {2} / {3}; {4}".format(
                process_in_per,
                load_cnt,
                gen_cnt,
                len_DIR,
                (datetime.now() - start_time).total_seconds()
            ))

    return np.array(datas_list), np.array(labels_list)


def single_img_to_numpy(img_path):
    trf = transforms.Compose([transforms.Resize((224, 224)),
                              transforms.ToTensor(),
                              transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])
    img = Image.open(img_path)
    img = trf(img)
    img = torch.unsqueeze(img, dim=0)
    net = torchvision.models.resnet18(pretrained=True)
    out = net(img)
    single_line_numpy = out.detach().cpu().numpy().reshape(-1)
    return single_line_numpy


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
    return os.path.exists(os.path.join(cache_path, DIR + ".csv"))


def store_numpy_cache(cache_path, DIR, np_array):
    csv_path = os.path.join(cache_path, DIR + ".csv")
    np.savetxt(csv_path, np_array, delimiter=",", fmt='%0.2f')


def load_numpy_cache(cache_path, DIR):
    csv_path = os.path.join(cache_path, DIR + ".csv")
    return np.genfromtxt(csv_path, delimiter=',').astype(np.float64)


if __name__ == '__main__':
    a, b = load_pics_and_labels_to_numpy(DATA_PATH, test_dict, CACHE_PATH)
    pass
