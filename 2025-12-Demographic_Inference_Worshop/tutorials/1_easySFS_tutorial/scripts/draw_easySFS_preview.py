import argparse
from matplotlib import pyplot as plt
import os

def draw_easySFS_preview(easySFS_preview_output, output=None):
    prev_line = None
    with open(easySFS_preview_output) as f:
        for line in f:
            if line.startswith("("):
                pairs = line.strip().split("\t")
                x, y = [], []
                for pair in pairs:
                    proj, n_sites = pair.strip()[1:-1].split(",")
                    proj = int(proj)
                    n_sites = float(n_sites)
                    x.append(proj)
                    y.append(n_sites)
                plt.figure(figsize=(3, 3))
                plt.plot(x, y, marker="o", color="black")
                plt.xlabel("Projection")
                plt.ylabel("Number of segregating sites")
                
                # Use previous line (should be population name) as title
                pop_title = prev_line.strip() if prev_line else ""
                plt.title("Population: " + pop_title)
                ymin, ymax = plt.ylim()
                plt.ylim(0, ymax)
                
                if output:
                    # Insert population to filename if pattern contains {pop}
                    if "{pop}" in output:
                        out_fn = output.format(pop=pop_title.replace(" ", "_"))
                    else:
                        out_fn = output
                    plt.savefig(out_fn, dpi=120)
                    print(f"[INFO] Saved: {out_fn}")
                    plt.close()
                else:
                    plt.show()
            prev_line = line

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot projection preview from easySFS preview output")
    parser.add_argument("easySFS_output", help="easySFS preview output file")
    parser.add_argument("-o", "--output", help="Output file for plot (if multiple populations, use {pop} to create one file per population)", default=None)
    args = parser.parse_args()
    draw_easySFS_preview(args.easySFS_output, output=args.output)
