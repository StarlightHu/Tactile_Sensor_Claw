import cv2
import os
from datetime import datetime

DELTA = 10
FPS = 100

SRC_PARENT_PATH = "/Volumes/USB128/4_30"
TAR_PARENT_PATH = "/Users/liujilan/fruit_pics"


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

    if not os.path.exists(TAR_PARENT_PATH):
        try:
            os.mkdir(TAR_PARENT_PATH)
        except FileNotFoundError:
            print("This is a hit by me:")
            print("Python does not support creating multi-level mkdir()")
            print("You should make sure that the grand-parent direction exists.")

    cnt = 0
    for fruit_data in os.listdir(SRC_PARENT_PATH):
        for video in os.listdir(os.path.join(SRC_PARENT_PATH, fruit_data)):
            if video.split(".")[-1].lower() == "avi":
                path = os.path.join(TAR_PARENT_PATH, fruit_data, video.split(".")[0])
                if not os.path.exists(os.path.join(TAR_PARENT_PATH, fruit_data)):
                    # os.mkdir不支持多级创建, 又不想为没有视频的文件夹创建, 所以在这里创建
                    os.mkdir(os.path.join(TAR_PARENT_PATH, fruit_data))
                if not os.path.exists(path):
                    os.mkdir(path)
                video_ins = cv2.VideoCapture(os.path.join(SRC_PARENT_PATH, fruit_data, video))
                video_to_pics(video_ins, path)
                video_ins.release()

        print(int(cnt * 100 / len(os.listdir(SRC_PARENT_PATH))), "%")
        cnt += 1
