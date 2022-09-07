import os

SRC_PARENT_PATH = "/Volumes/USB128/2"
TAR_PARENT_PATH = "/Volumes/USB128/pic_data/2"


if __name__ == '__main__':
    for DIR in os.listdir(os.path.join(SRC_PARENT_PATH)):
        os.system("mv {} {}".format(
            os.path.join(SRC_PARENT_PATH, DIR, "info.txt"),
            os.path.join(TAR_PARENT_PATH, DIR, "info.txt")
        ))