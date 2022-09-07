import os
import cv2

SRC_PARENT_PATH = "/Volumes/USB128/pic_data/5"
TAR_PARENT_PATH = "/Volumes/USB128/train_pic/5"

PIC_NUM = 6


def choose_pics(DIR_path, use_info=False):
    if use_info:
        start, end = choose_pics_due_info(DIR_path)
    else:
        start = 0
        end = len(os.listdir(os.path.join(DIR_path, "0"))) - 1

    delta = int((end - start + 1) / PIC_NUM)
    tail = int((PIC_NUM + 1) / 2)
    front = PIC_NUM - tail

    res = []

    for i in range(front):
        res.append(start + i * delta)

    for i in range(tail):
        res.append(end - i * delta)

    return res


def choose_pics_due_info(DIR_path):
    fl = open(os.path.join(DIR_path, "info.txt"))
    start, end = [], []
    for _ in range(3):
        fl.readline()   # 空读
    for _ in range(3):
        content = fl.readline()
        tmp = content.split("\n")[0].split(":")[-1].split(",")
        try:
            start.append(int(tmp[0]))
            end.append(int(tmp[1]))
        except ValueError:
            print(tmp)
            print(DIR_path)
            print("Oh Shit!")
            exit(0)


    return max(start), min(end)


def change_grey(SRC_PATH, TAR_PATH):
    img = cv2.imread(SRC_PATH, 0)  # 以灰度模式打开图片(无论是否是彩图)
    try:
        result = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    except Exception as e:
        print(SRC_PATH)
        raise e

    # cv2.imshow('result', result)
    cv2.imwrite(TAR_PATH, result)


if __name__ == '__main__':
    if not os.path.exists(SRC_PARENT_PATH):
        print("Source path does not exist.")
        exit(0)

    if not os.path.exists(TAR_PARENT_PATH):
        try:
            os.mkdir(TAR_PARENT_PATH)
        except FileNotFoundError:
            print("This is a hit by me:")
            print("Python does not support creating multi-level mkdir()")
            print("You should make sure that the grand-parent direction exists.")

    lenght = len(os.listdir(SRC_PARENT_PATH))
    for i, DIR in enumerate(os.listdir(SRC_PARENT_PATH)):
        if not os.path.exists(os.path.join(TAR_PARENT_PATH, DIR)):
            os.mkdir(os.path.join(TAR_PARENT_PATH, DIR))
        os.system("cp {} {}".format(os.path.join(SRC_PARENT_PATH, DIR, "info.txt"),
                                     os.path.join(TAR_PARENT_PATH, DIR, "info.txt")))

        # need_pics = choose_pics(os.path.join(SRC_PARENT_PATH, DIR))
        need_pics = choose_pics(os.path.join(SRC_PARENT_PATH, DIR), True)
        for VIDEO in range(3):
            if not os.path.exists(os.path.join(TAR_PARENT_PATH, DIR, str(VIDEO))):
                os.mkdir(os.path.join(TAR_PARENT_PATH, DIR, str(VIDEO)))
            for j, pics in enumerate(need_pics):
                pic_src_name = str(pics).zfill(10) + ".jpg"
                pic_tar_name = str(j).zfill(10) + ".jpg"

                # os.system("cp {} {}/".format(os.path.join(SRC_PARENT_PATH, DIR, str(VIDEO), pic_name),
                #                              os.path.join(TAR_PARENT_PATH, DIR, str(VIDEO), pic_name)))
                change_grey(os.path.join(SRC_PARENT_PATH, DIR, str(VIDEO), pic_src_name),
                            os.path.join(TAR_PARENT_PATH, DIR, str(VIDEO), pic_tar_name))

        print("{0} / {1}, {2}%".format(i + 1, lenght, int((i + 1) * 100 / lenght)))
