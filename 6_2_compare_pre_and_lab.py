import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score

LAB_PATH = "./lab.txt"
PER_PATH = "./pre.txt"


#  test = CompareVimer(LAB_PATH, PER_PATH, 1)

class CompareVimer:
    def __init__(self, lab_path, pre_path, period=None, left=None, right=None):
        self.cnt = 0
        self.lab_path = lab_path
        self.pre_path = pre_path
        self.period = period
        self.left = left
        self.right = right

    def count(self, new_period=None):
        self.cnt += 1

        if new_period is not None:
            self.period = new_period

        if self.period is None:
            return

        if self.cnt != 0 and self.cnt % self.period == 0:
            self.show()

    def show(self):
        if not os.path.exists(self.pre_path):
            print("pre_path doesn't exists")

        if not os.path.exists(self.lab_path):
            print("lab_path doesn't exists")

        pre = np.genfromtxt(self.pre_path, delimiter=',').astype(np.float64)

        lab = np.genfromtxt(self.lab_path, delimiter=',').astype(np.float64)

        lab = lab.reshape((-1, 6), order="C")[:, 1]

        plt.cla()

        plt.xlabel("label")
        plt.ylabel("predict")

        max_ticks = int(max(np.max(lab), np.max(pre))) + 10

        x_y_line = np.arange(0, max_ticks, 10)
        plt.plot(x_y_line, x_y_line, 'r--')
        plt.plot(x_y_line, x_y_line - 10, 'y--')
        plt.plot(x_y_line, x_y_line + 10, 'y--')

        plt.xticks(np.arange(0, max_ticks, 5))
        plt.yticks(np.arange(0, max_ticks, 5))

        sub_aim_lab = []
        sub_aim_pre = []
        sub_remain_lab = []
        sub_remain_pre = []

        def between_l_r(num, l, r):
            l_flag = True
            r_flag = True
            if l is not None:
                l_flag = l <= num
            if r is not None:
                r_flag = r >= num
            return l_flag and r_flag

        for i, label in enumerate(lab):
            if between_l_r(label, self.left, self.right):
                sub_aim_lab.append(lab[i])
                sub_aim_pre.append(pre[i])
            else:
                sub_remain_lab.append(lab[i])
                sub_remain_pre.append(pre[i])

        # plt.scatter(lab, pre, sizes=[5 for _ in range(len(lab))])
        plt.scatter(sub_aim_lab, sub_aim_pre,
                    sizes=[5 for _ in range(len(sub_aim_lab))],
                    color=['b' for _ in range(len(sub_aim_lab))])
        plt.scatter(sub_remain_lab, sub_remain_pre,
                    sizes=[5 for _ in range(len(sub_remain_lab))],
                    color=['c' for _ in range(len(sub_remain_lab))])

        r2_all = r2_score(lab, pre)
        r2_aim = r2_score(sub_aim_lab, sub_aim_pre)

        plt.title("All R^2={:.4f};   [{}, {}] R^2={:.4f}".format(
            r2_all, self.left, self.right, r2_aim))
        plt.show()


if __name__ == '__main__':
    test = CompareVimer(LAB_PATH, PER_PATH, 1, 20, 60)
    test.show()
