import os
import numpy as np
import matplotlib.pyplot as plt

LABEL_PATH = "/Volumes/USB128/lab_data"


def read_from_path(parent_dir):
    if not os.path.exists(LABEL_PATH):
        print("Source path does not exist.")
        exit(0)

    label_set = []

    for SET in os.listdir(os.path.join(LABEL_PATH)):
        if SET[0] == ".":  # 跳过隐藏文件
            continue
        read_from_file(os.path.join(LABEL_PATH, SET), label_set)

    return label_set


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


if __name__ == '__main__':
    fruit_with_multi_label = read_from_path(LABEL_PATH)
    data = fruit_with_multi_label
    all_data = [x for arr in data for x in arr]
    avg_data = [sum(arr) / len(arr) for arr in data]
    analysis(all_data, 5, "All Result Datas")
    analysis(avg_data, 5, "Average Result per Fruit Datas")
