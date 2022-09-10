import cv2
import os
from datetime import datetime

DELTA = 10
FPS = 100

SRC_PARENT_PATH = "/Volumes/USB128/raw_data/7"
TAR_PARENT_PATH = "/Volumes/USB128/pic_data/7"


def video_to_pics(video, parent_path):
    cnt = 0
    while True:
        ret, frame = video.read()

        if ret:
            name = str(cnt).zfill(10) + ".jpg"
            path = os.path.join(parent_path, name)
            # 保存png图像，图像后缀必须为.png，图像质量0-9，默认为3，0质量最好，9最差
            # cv2.imwrite(path, frame, [cv2.IMWRITE_PNG_COMPRESSION, 0])
            # 保存jpg图像，图像后缀必须为.jpg，图像质量0-100，默认为95,100最好，0最差
            cv2.imwrite(path, frame, [cv2.IMWRITE_JPEG_QUALITY, 100])
            cnt += 1
        else:
            break


if __name__ == '__main__':
    if not os.path.exists(SRC_PARENT_PATH):
        print("Source path does not exist.")
        exit(0)

    if not os.path.exists(os.path.join(SRC_PARENT_PATH, "info.txt")):
        print("No info file!")
        exit(0)

    if not os.path.exists(TAR_PARENT_PATH):
        try:
            os.mkdir(TAR_PARENT_PATH)
        except FileNotFoundError:
            print("This is a hit by me:")
            print("Python does not support creating multi-level mkdir()")
            print("You should make sure that the grand-parent direction exists.")

    fl = open(os.path.join(SRC_PARENT_PATH, "info.txt"), "r")
    content = fl.readline()
    fl.close()
    SET = int(content.split("\n")[0].split(":")[-1])

    lenght = len(os.listdir(SRC_PARENT_PATH))
    for i, fruit_data in enumerate(os.listdir(SRC_PARENT_PATH)):
        if not os.path.isdir(os.path.join(SRC_PARENT_PATH, fruit_data)):
            print("{0} / {1}, {2}%".format(i + 1, lenght, int((i + 1) * 100 / lenght)))
            continue

        for video in os.listdir(os.path.join(SRC_PARENT_PATH, fruit_data)):
            fl = open(os.path.join(SRC_PARENT_PATH, fruit_data, "info.txt"))
            content = fl.readline()
            INDEX = int(content.split("\n")[0].split(":")[-1])
            content = fl.readline()
            LABEL = int(content.split("\n")[0].split(":")[-1])
            fl.close()

            if video.split(".")[-1].lower() == "avi":
                path = os.path.join(TAR_PARENT_PATH, fruit_data, video.split(".")[0])

                if not os.path.exists(os.path.join(TAR_PARENT_PATH, fruit_data)):
                    # os.mkdir不支持多级创建, 又不想为没有视频的文件夹创建, 所以在这里创建
                    os.mkdir(os.path.join(TAR_PARENT_PATH, fruit_data))

                    fl = open(os.path.join(TAR_PARENT_PATH, fruit_data, "info.txt"), "w")
                    fl.write("set: {}\nindex: {}\nlabel: {}\n".format(SET, INDEX, LABEL))
                    fl.write("0: , \n1: , \n2: , \n")
                    fl.close()

                if not os.path.exists(path):
                    os.mkdir(path)
                video_ins = cv2.VideoCapture(os.path.join(SRC_PARENT_PATH, fruit_data, video))
                video_to_pics(video_ins, path)
                video_ins.release()

        print("{0} / {1}, {2}%".format(i + 1, lenght, int((i + 1) * 100 / lenght)))
