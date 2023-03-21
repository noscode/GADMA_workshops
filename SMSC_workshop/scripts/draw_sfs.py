import dadi
from matplotlib import pyplot as plt
import matplotlib
import moments
import os
import sys
import numpy as np
from matplotlib.cm import ScalarMappable

cmap = plt.cm.get_cmap('hsv')  # load color scheme
figsize=(6,5)

def draw_1d_sfs(input_file):
    # Read data using dadi
    fs = dadi.Spectrum.from_file(input_file)

    # Create canvas
    plt.figure(figsize=figsize)
    ax = plt.gca()
    
    # Draw SFS as colored bins
    # We ignore first and last positions of FS
    vmax = np.max(fs)*(1+1e-3)
    colors = cmap([np.log(val) / np.log(vmax) for val in fs[1:-1]])
    plt.bar(range(1, len(fs)-1), fs[1:-1], color=colors, width=1)

    # Draw colorbar
    sm = ScalarMappable(cmap=cmap, norm=matplotlib.colors.LogNorm(vmin=1e-3, vmax=vmax))
    sm.set_array([])
    cbar = plt.colorbar(sm)
    cbar.ax.tick_params(labelsize=20)

    # Some other adjustments for plot
    plt.xlim(-0.5, len(fs)+0.5)
    plt.xlabel("Allele frequency", fontsize=25)
    plt.ylabel("Count", fontsize=25)
    # We change the fontsize of minor ticks label
    ax.tick_params(axis='both', which='major', labelsize=20)
    ax.tick_params(axis='both', which='minor', labelsize=20)
    plt.tight_layout()
    plt.show()


def draw_2d_sfs(input_file):
    # Read data using dadi
    fs = dadi.Spectrum.from_file(input_file)

    # Create canvas
    plt.figure(figsize=figsize)
    ax = plt.gca()

    # Plot SFS using function from dadi
    dadi.Plotting.plot_single_2d_sfs(
        fs,
        ax=ax,
        vmin=1,
        vmax=None,
        colorbar=True,
        cmap=cmap
    )
                
    # Change font size on colorbar
    ax.figure.dadi_colorbars[0].ax.tick_params(labelsize=20)
   
    # Final adjustments
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.tight_layout()
    plt.show()


def draw_3d_sfs(input_file):
    # Read data using dadi
    fs = dadi.Spectrum.from_file(input_file)

    plt.figure(figsize=figsize)
    dadi.Plotting.plot_3d_spectrum(
        fs,
        fignum=3,
        vmin=1,
        vmax=None,
        show=False
    )
    
    plt.tight_layout()
    plt.show()
    
    
def draw_sfs(input_file):
    # Read data using dadi
    fs = dadi.Spectrum.from_file(input_file)
    
    if len(fs.pop_ids) == 1:
        draw_1d_sfs(input_file)
    elif len(fs.pop_ids) == 2:
        draw_2d_sfs(input_file)
    elif len(fs.pop_ids) == 3:
        draw_3d_sfs(input_file)
    else:
        raise ValueError("This SFS could not be drawn by this script.")


# Command line interface
if __name__ == "__main__":
    # Check that we have requered option
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <dadi_sfs_file.fs>")
        os._exit(1)
    draw_sfs(sys.argv[1])
