import sys
import os
from matplotlib import pyplot as plt

def draw_Ne_result(ne_file):
    plt.figure(figsize=(5, 2))
    sizes = []
    with open(ne_file) as f:
        next(f)
        next(f)
        for line in f:
            sizes.append(float(line.split()[-1]))
    plt.plot(range(len(sizes)), sizes, color="k")
    plt.xlabel("Time (generations)")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <gone_Ne_output>")
    else:
        draw_Ne_result(sys.argv[1])
