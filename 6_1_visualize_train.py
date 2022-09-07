import numpy as np
import matplotlib.pyplot as plt



class DataViwer:
    def __init__(self, period=None, title=None):
        self.cnt = 0
        self.datas = []
        self.period = period
        self.title = title

    def add_data(self, new_data, new_period=None):
        self.cnt += 1
        self.datas.append(new_data)

        if new_period is not None:
            self.period = new_period

        if self.period is None:
            return

        if self.cnt != 0 and self.cnt % self.period == 0:
            self.show()

    def show(self):
        plt.cla()
        plt.plot(np.arange(len(self.datas)), np.array(self.datas))
        if self.title is not None:
            plt.title(self.title)
        plt.show()


if __name__ == '__main__':
    dw = DataViwer(40, "abc")
    for _ in range(100):
        dw.add_data(np.random.random())

    pass

