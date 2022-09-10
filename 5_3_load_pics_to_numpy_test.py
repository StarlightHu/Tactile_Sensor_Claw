import os
from datetime import datetime

def load_pics_and_labels_to_numpy_test(datas_path, labels_dict):
    print("Test Load start")
    if not os.path.exists(datas_path):
        raise Exception("Datas path does not exist.")

    notice_time = 5  # 控制打印进度的
    len_DIR = len(os.listdir(os.path.join(datas_path)))
    start_time = datetime.now()
    print("Start at {}.".format(start_time.strftime('%Y_%m_%d_%H_%M_%S_%f')))
    pre_pro = None
    for process, DIR in enumerate(os.listdir(os.path.join(datas_path))):
        if DIR[0] == ".":  # 跳过隐藏文件
            continue

        SET, LABEL = get_info_set_and_label(os.path.join(datas_path, DIR))
        # str, int SET = 1, 2, 3, 4... LABEL = 1, 2, 3, 4...
        try:
            if labels_dict[SET][LABEL - 1] is None:
                continue
        except Exception as e:
            print("What's going on ?!?!")
            print("path: {}, set: {}, label {}".format(DIR, SET, LABEL))
            raise e

        for i in range(3):
            for j in range(6):
                video_name = str(i)
                pic_name = str(j).zfill(10) + ".jpg"
                single_img_to_numpy_test(os.path.join(
                    datas_path,
                    DIR,
                    video_name,
                    pic_name))

        process_in_per = int((process + 1) * 100 / len_DIR)
        if process_in_per != 0 and process_in_per % notice_time == 0:
            if pre_pro != process_in_per:
                print("{0}%; {1} / {2}; {3}".format(
                    process_in_per,
                    process,
                    len_DIR,
                    (datetime.now() - start_time).total_seconds()
                ))
                pre_pro = process_in_per

    print("Test Load is OK")

def single_img_to_numpy_test(img_path):
    if not os.path.exists(img_path):
        print(img_path)
        print("Oh shit")
        raise Exception("Image path does not exist.")

if __name__ == '__main__':