import cv2
import os
from datetime import datetime

DELTA = 20
FPS = 50


# from PyCameraList.camera_device import test_list_cameras, list_video_devices, list_audio_devices
# pip install pycameralist


def open_camera(caps, parent_path, timer=3):
    for i in range(len(caps)):
        caps[i].set(cv2.CAP_PROP_FOURCC,
                    cv2.VideoWriter.fourcc('M', 'J', 'P', 'G'))  # 视频流格式
        caps[i].set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        caps[i].set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    fourcc = cv2.VideoWriter_fourcc(*'XVID')

    out_paths = []
    for i in range(len(caps)):
        out_paths.append(os.path.join(parent_path, (str(i) + '.avi')))

    for i in range(len(caps)):
        ret, frame = caps[i].read()
        if not ret:
            print("port{} is empty\n".format(i))

    # assert ret1 and ret2 and ret3 == True

    outs = []
    for i in range(len(caps)):
        outs.append(cv2.VideoWriter(out_paths[i], fourcc, FPS, (640, 480)))

    titles = []
    for i in range(len(caps)):
        titles.append("image" + str(i))

    while True:
        for i in range(len(caps)):
            ret, frame = caps[i].read()

            if ret:
                cv2.imshow(titles[i], frame)

        key = cv2.waitKey(DELTA) & 0xff

        if key == ord('q'):
            break

        if key == ord('b'):
            while True:
                for i in range(len(caps)):
                    ret, frame = caps[i].read()

                    if ret:
                        outs[i].write(frame)
                        cv2.imshow(titles[i], frame)

                key = cv2.waitKey(DELTA) & 0xff

                if key == ord('q'):
                    break

            break

        if key == ord('t'):
            start = datetime.now()

            while True:
                for i in range(len(caps)):
                    ret, frame = caps[i].read()

                    if ret:
                        outs[i].write(frame)
                        cv2.imshow(titles[i], frame)

                key = cv2.waitKey(DELTA) & 0xff

                if (datetime.now() - start).total_seconds() > timer:
                    break

            break


def scan_ports(caps, cnt=10):
    ls = []
    """
    for i in range(cnt):
        cap = cv2.VideoCapture(i)
        ret, frame = cap.read()
        if ret:
            ls.append(i)
            caps.append(cap)
        else:
            cap.release()
        
        
    os.system("clear")
    print("Next ports may be OK:")
    print(ls)
    print("The first two one may be the local camera.")
    """
    caps.append(cv2.VideoCapture(0))
    caps.append(cv2.VideoCapture(2))
    caps.append(cv2.VideoCapture(4))


if __name__ == '__main__':
    caps = []

    scan_ports(caps, 30)

    # assert len(caps) >= 3
    # ports = caps[-3:]
    # assert len(ports) == 3
    ports = caps

    path = './fruit_data/'
    if not os.path.exists(path):
        os.mkdir(path)

    now_time = datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')
    save_path = os.path.join(path, now_time)
    os.mkdir(save_path)

    open_camera(ports, save_path)

    for cap in caps:
        cap.release()
    cv2.destroyAllWindows()
    
    content = input("Enter your fruit number:")
    file = open(os.path.join(save_path, "info.txt"), "w+")
    meg = "fruit num: " + content + "\n"
    file.write(meg)
    file.close()
