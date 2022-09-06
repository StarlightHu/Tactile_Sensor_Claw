import os
import numpy as np
import matplotlib.pyplot as plt

LABEL_PATH = "/Volumes/USB128/lab_data"


def load_labels_to_memomery(labels_path, is_preview=False):
    if not os.path.exists(labels_path):
        raise Exception("Labels path does not exist.")

    labels_dict = {}

    for SET in os.listdir(os.path.join(labels_path)):
        if SET[0] == ".":  # 跳过隐藏文件
            continue

        SET_name = SET.split(".")[0]
        if SET_name not in labels_dict:
            labels_dict[SET_name] = []
        read_from_file(os.path.join(labels_path, SET), labels_dict[SET_name])

    if is_preview:
        preview_labels(labels_dict)


    labels_dict_with_mean = {}
    for key in labels_dict:
        labels_dict_with_mean[key] = []
        for ls in labels_dict[key]:
            if ls[0] is None:
                labels_dict_with_mean[key].append(None)
            else:
                labels_dict_with_mean[key].append(np.mean(np.array(ls)))



    return labels_dict_with_mean



def read_from_file(file_path, ls):
    fl = open(file_path)

    while True:
        line = fl.readline()

        if line == "":
            break

        line_without_n = line.split("\n")[0]
        if line_without_n == "":
            continue

        commit = line_without_n.split("#")
        if len(commit) > 1:  # 被标记
            ls.append([None])  # 填None
            continue

        label_line = commit[0]
        index_and_labels = label_line.split(":")
        if len(index_and_labels) < 2:
            continue

        labels = index_and_labels[-1].split(" ")

        ls.append([])
        for label in labels:
            if label != "":
                ls[-1].append(float(label))

    fl.close()


def get_bar(ls, step, start=None, title=None):
    if start is None:
        start = int(min(ls))
    else:
        if start > int(min(ls)):
            print("指定的起点太大, 我还没写处理")
            exit(0)

    end = int(max(ls)) + 1

    names = [str(x) for x in range(start, end, step)]
    width = 0.75
    x_ticks = np.arange(len(names))
    # x_ticks一定要用numpy, 因为要做矩阵操作

    values = [0 for _ in range(len(names))]
    for var in ls:
        values[int((var - start) / step)] += 1

    # fig, ax = plt.subplots()
    # bar = plt.bar(names, values)
    bar = plt.bar(x_ticks + width / 2, values, width)  # 默认居中, 所以加1/2
    plt.xticks(x_ticks, names)  # 还原names
    plt.bar_label(bar, label_type="edge")
    if title is not None:
        plt.title(title)
    plt.show()


def analysis(ls, step=5, title=None):
    get_bar(ls, step, int(min(ls) / step) * step, title)


def preview_labels(labels_dict, step=5):
    all_data = [x
                for key in labels_dict
                for arr in labels_dict[key]
                for x in arr
                if x is not None]  # 我们将None异常算入
    avg_data = [sum(arr) / len(arr)
                for key in labels_dict
                for arr in labels_dict[key]
                if arr[0] is not None]
    analysis(all_data, step, "All Result Datas")
    analysis(avg_data, step, "Average Result per Fruit Datas")


if __name__ == '__main__':
    test_dict = load_labels_to_memomery(LABEL_PATH, True)
    pass
