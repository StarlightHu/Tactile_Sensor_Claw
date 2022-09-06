import os

def load_pics_and_labels_to_numpy_test(datas_path, labels_dict):
    if not os.path.exists(datas_path):
        raise Exception("Datas path does not exist.")

    for DIR in os.listdir(os.path.join(datas_path)):
        if DIR[0] == ".":  # 跳过隐藏文件
            continue

        SET, LABEL = get_info_set_and_label(os.path.join(datas_path, DIR))
        # str, int SET = 1, 2, 3, 4... LABEL = 1, 2, 3, 4...
        if labels_dict[SET][LABEL - 1] is None:
            continue
        for i in range(3):
            for j in range(6):
                video_name = str(i)
                pic_name = str(j).zfill(10) + ".jpg"
                single_img_to_numpy_test(os.path.join(
                    datas_path,
                    DIR,
                    video_name,
                    pic_name))

def single_img_to_numpy_test(img_path):
    if not os.path.exists(img_path):
        print(img_path)
        print("Oh shit")
        raise Exception("Image path does not exist.")

if __name__ == '__main__':