from matplotlib import pyplot as plt
import matplotlib
import moments
import os
import sys
import numpy as np
from matplotlib.cm import ScalarMappable
import argparse

cmap = plt.get_cmap('hsv')  # load color scheme
figsize = (6, 5)

def draw_1d_sfs(input_file, output=None):
    fs = moments.Spectrum.from_file(input_file)
    plt.figure(figsize=figsize)
    ax = plt.gca()
    vmax = np.max(fs)*(1+1e-3)
    colors = cmap([np.log(val) / np.log(vmax) for val in fs[1:-1]])
    plt.bar(range(1, len(fs)-1), fs[1:-1], color=colors, width=1)
    sm = ScalarMappable(cmap=cmap, norm=matplotlib.colors.LogNorm(vmin=1, vmax=vmax))
    cbar = plt.colorbar(sm)
    cbar.ax.tick_params(labelsize=20)
    plt.xlim(-0.5, len(fs)+0.5)
    plt.xlabel("Allele frequency", fontsize=25)
    plt.ylabel("Count", fontsize=25)
    ax.tick_params(axis='both', which='major', labelsize=20)
    ax.tick_params(axis='both', which='minor', labelsize=20)
    plt.tight_layout()
    if output:
        plt.savefig(output, dpi=120)
        print(f"[INFO] Saved: {output}")
        plt.close()
    else:
        plt.show()

def draw_2d_sfs(input_file, output=None):
    fs = moments.Spectrum.from_file(input_file)
    plt.figure(figsize=figsize)
    ax = plt.gca()
    moments.Plotting.plot_single_2d_sfs(
        fs,
        ax=ax,
        vmin=1,
        vmax=None,
        colorbar=True,
        cmap=cmap,
        out=None,
    )
    ax.figure.moments_colorbars[0].ax.tick_params(labelsize=20)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.tight_layout()
    if output:
        plt.savefig(output, dpi=120)
        print(f"[INFO] Saved: {output}")
        plt.close()
    else:
        plt.show()

def draw_3d_sfs(input_file, output=None):
    fs = moments.Spectrum.from_file(input_file)
    fig = plt.figure(figsize=figsize)
    moments.Plotting.plot_3d_spectrum(
        fs,
        fignum=3,
        vmin=1,
        vmax=None,
        show=False
    )
    plt.tight_layout()
    if output:
        plt.savefig(output, dpi=120)
        print(f"[INFO] Saved: {output}")
        plt.close()
    else:
        plt.show()
    
def draw_sfs(input_file, output=None):
    fs = moments.Spectrum.from_file(input_file)
    if len(fs.pop_ids) == 1:
        draw_1d_sfs(input_file, output=output)
    elif len(fs.pop_ids) == 2:
        draw_2d_sfs(input_file, output=output)
    elif len(fs.pop_ids) == 3:
        draw_3d_sfs(input_file, output=output)
    else:
        raise ValueError("This SFS could not be drawn by this script.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot 1d/2d/3d dadi/moments SFS and either display or save to file.")
    parser.add_argument("dadi_sfs_file", help="dadi SFS file")
    parser.add_argument("-o", "--output", help="Output file for plot (optional, otherwise pops up a window)", default=None)
    args = parser.parse_args()
    draw_sfs(args.dadi_sfs_file, output=args.output)
