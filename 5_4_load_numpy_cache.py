import os
import numpy as np
import matplotlib.pyplot as plt


def have_cached(cache_path, DIR):
    return os.path.exists(os.path.join(cache_path, DIR + ".csv"))


def store_numpy_cache(cache_path, DIR, np_array):
    csv_path = os.path.join(cache_path, DIR + ".csv")
    np.savetxt(csv_path, np_array, delimiter=",", fmt='%0.2f')


def load_numpy_cache(cache_path, DIR):
    csv_path = os.path.join(cache_path, DIR + ".csv")
    return np.genfromtxt(csv_path, delimiter=',').astype(np.float)


if __name__ == '__main__':
    pass
