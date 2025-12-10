import argparse
from matplotlib import pyplot as plt
import math

def parse_easySFS_preview_file(filepath):
    populations = []
    pop_names = []
    current_pop = None
    with open(filepath) as f:
        for line in f:
            if line.startswith('('):
                # Data line
                pairs = line.strip().split("\t")
                x, y = [], []
                for pair in pairs:
                    proj, n_sites = pair.strip()[1:-1].split(",")
                    x.append(int(proj))
                    y.append(float(n_sites))
                if current_pop:
                    populations.append((current_pop, x, y))
                    current_pop = None  # reset until next pop name line
            else:
                # Population label line
                current_pop = line.strip()
    return populations

def plot_populations(populations, output=None):
    num_pops = len(populations)
    if num_pops == 0:
        print("[ERROR] No populations found.")
        return

    ncols = min(3, num_pops)  # up to 3 columns for a grid
    nrows = math.ceil(num_pops / ncols)
    fig, axes = plt.subplots(nrows, ncols, figsize=(4 * ncols, 4 * nrows), squeeze=False)
    plt.subplots_adjust(hspace=0.4, wspace=0.4)
    
    for idx, (pop_name, x, y) in enumerate(populations):
        ax = axes[idx // ncols][idx % ncols]
        ax.plot(x, y, marker="o", color="black")
        ax.set_xlabel("Projection")
        ax.set_ylabel("Segregating sites")
        ax.set_title(f"Population: {pop_name}")
        ymin, ymax = ax.get_ylim()
        ax.set_ylim(0, ymax)
    # Hide unused subplots
    for j in range(num_pops, nrows * ncols):
        fig.delaxes(axes[j // ncols][j % ncols])

    fig.tight_layout()
    if output:
        plt.savefig(output, dpi=120)
        print(f"[INFO] Saved: {output}")
        plt.close()
    else:
        plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot projection preview from easySFS preview output (all populations as subplots)")
    parser.add_argument("easySFS_output", help="easySFS preview output file")
    parser.add_argument("-o", "--output", help="Output file for combined subplot image (default: show interactively)", default=None)
    args = parser.parse_args()
    populations = parse_easySFS_preview_file(args.easySFS_output)
    plot_populations(populations, output=args.output)
