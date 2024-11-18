from matplotlib import pyplot as plt
import os
import sys

def draw_easySFS_preview(easySFS_preview_output):
    # Draw result for easySFS output
    prev_line = None
    with open(easySFS_preview_output) as f:
        for line in f:
            # If line startswith "(" we consider it has projections info we need
            if line.startswith("("):
                # split line by tabs
                pairs = line.strip().split("\t")
                # create lists for plot
                x, y = [], []
                # read each pair in line and add information to our lists
                for pair in pairs:
                    proj, n_sites = pair.strip()[1:-1].split(",")
                    proj = int(proj)
                    n_sites = float(n_sites)
                    x.append(proj)
                    y.append(n_sites)
                # Now we can draw our plot.
                # We draw it here because easySFS could have information
                # for several populations.
                plt.figure(figsize=(3, 3))
                plt.plot(x, y, marker="o", color="black")
                plt.xlabel("Projection")
                plt.ylabel("The number of segregating sites")
                plt.title("Population: " + prev_line.strip())
                ymin, ymax = plt.ylim()
                plt.ylim(0, ymax)
                plt.show()
            prev_line = line

# Command line interface
if __name__ == "__main__":
    # Check that we have requered option
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <easySFS_output>")
        os._exit(1)
    draw_easySFS_preview(sys.argv[1])
