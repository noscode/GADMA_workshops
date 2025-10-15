import argparse
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from scipy import stats
import os

def read_popmap(popmap_filename):
    pop2ind = {}
    sample2pop = {}
    with open(popmap_filename) as f:
        for line in f:
            if not line.strip(): continue
            sample, pop = line.strip().split()
            if pop not in pop2ind:
                pop2ind[pop] = len(pop2ind)
            sample2pop[sample] = pop
    return pop2ind, sample2pop

def get_data_for_ternary_plot(vcf_filename, samples, vcf_strip_suffix=False):
    data = []
    with open(vcf_filename) as f:
        for line in f:
            if line.startswith("#") and not line.startswith("##"):
                all_sample_names = line.strip().split()[9:]
                name_map = {}
                for name in all_sample_names:
                    match_name = name
                    if vcf_strip_suffix:
                        match_name = name.split('_')[0]
                    if match_name in samples:
                        name_map[name] = match_name
                sample_names = [name_map[name] for name in all_sample_names if name in name_map]
                sample_indices = [9 + i for i, name in enumerate(all_sample_names) if name in name_map]
            if line.startswith("#"):
                continue
            spl_line = line.strip().split()
            genotypes = [spl_line[i][:3] for i in sample_indices]
            valid_genotypes = []
            for genotype in genotypes:
                if genotype[0] == "." or genotype[2] == ".":
                    continue
                valid_genotypes.append(genotype)
            if not valid_genotypes:
                continue
            n_heteroz = sum((g[0] != g[2]) for g in valid_genotypes if g[0] in "01" and g[2] in "01")
            heteroz_value = n_heteroz / len(valid_genotypes)
            allele_freq = sum((g[0] == "0") + (g[2] == "0") for g in valid_genotypes)
            freq_value = allele_freq / (2 * len(valid_genotypes))
            data.append([freq_value, heteroz_value])
    return sample_names, np.array(data)

def xy_inside_triangle(xx, yy):
    corners = np.array([[-1/np.sqrt(3), 0], [0, 1], [1/np.sqrt(3), 0]])
    def barycentric(x, y):
        detT = (corners[1,1] - corners[2,1]) * (corners[0,0] - corners[2,0]) + \
               (corners[2,0] - corners[1,0]) * (corners[0,1] - corners[2,1])
        l1 = ((corners[1,1] - corners[2,1]) * (x - corners[2,0]) + (corners[2,0] - corners[1,0]) * (y - corners[2,1])) / detT
        l2 = ((corners[2,1] - corners[0,1]) * (x - corners[2,0]) + (corners[0,0] - corners[2,0]) * (y - corners[2,1])) / detT
        l3 = 1.0 - l1 - l2
        return l1, l2, l3
    mask = []
    for x, y in zip(xx, yy):
        l1, l2, l3 = barycentric(x, y)
        mask.append((l1 >= -1e-6) & (l2 >= -1e-6) & (l3 >= -1e-6))
    return np.array(mask)

def fill_hwe_background(ax, txp, y_lo, y_up):
    # Triangle corners, for reference
    left_corner = (-1/np.sqrt(3), 0)
    top_corner  = (0, 1)
    right_corner = (1/np.sqrt(3), 0)

    def get_poly_coords(region):
        if region == 'below':
            poly_x = np.concatenate([[left_corner[0]], txp, [right_corner[0]]])
            poly_y = np.concatenate([[left_corner[1]], y_lo, [right_corner[1]]])
        elif region == 'above':
            poly_x = np.concatenate([[top_corner[0]], txp[::-1], [top_corner[0]]])
            poly_y = np.concatenate([[top_corner[1]], y_up[::-1], [top_corner[1]]])
        elif region == 'between':
            poly_x = np.concatenate([[right_corner[0]], txp, [left_corner[0]], txp[::-1]])
            poly_y = np.concatenate([[right_corner[1]], y_up, [left_corner[1]], y_lo[::-1]])
        else:
            raise ValueError(region)
        mask = xy_inside_triangle(poly_x, poly_y)
        return poly_x[mask], poly_y[mask]
    bx, by = get_poly_coords('below')
    ax.fill(bx, by, color='red', alpha=0.13, zorder=0)
    bx, by = get_poly_coords('above')
    ax.fill(bx, by, color='red', alpha=0.13, zorder=0)
    bx, by = get_poly_coords('between')
    ax.fill(bx, by, color='limegreen', alpha=0.18, zorder=0)

# Pick pretty log ticks between min/max count (e.g. 1, 10, 100, 1000, etc.)
def pretty_log_ticks(min_c, max_c):
    min_pow = int(np.floor(np.log10(max(min_c, 1))))
    max_pow = int(np.ceil(np.log10(max_c)))
    ticks = [int(10 ** p) for p in range(min_pow, max_pow + 1)]
    # Also include actual min/max if out of range
    if min_c < ticks[0]: ticks = [min_c] + ticks
    if max_c > ticks[-1]: ticks = ticks + [max_c]
    return ticks

def hwe_ternary_plot(vcf_file, popmap_file, population_name, output_file=None, double_ids=True):
    pop2ind, sample2pop = read_popmap(popmap_file)
    if population_name not in pop2ind:
        print(f"[ERROR] Population '{population_name}' not found in {popmap_file}")
        exit(2)
    samples = [s for s in sample2pop if sample2pop[s] == population_name]
    if not samples:
        print(f"[ERROR] No samples for population '{population_name}' in {popmap_file}")
        exit(3)
    samples, data = get_data_for_ternary_plot(vcf_file, samples, double_ids)
    if len(data) == 0:
        print("[ERROR] No usable SNP/genotype data for selected population.")
        exit(4)
    u, c = np.unique(data, axis=0, return_counts=True)
    color = [np.log(n) for n in c] if np.any(c > 1) else [1]*len(u)
    log_ticks = [0, np.log(10), np.log(100), np.log(1000), np.log(10000)]
    x = u[:,0]
    y = u[:,1]
    tx = (-2*x + 1)/np.sqrt(3)
    ty = y

    inside_mask = xy_inside_triangle(tx, ty)
    tx, ty, color = tx[inside_mask], ty[inside_mask], np.array(color)[inside_mask]

    fig, ax = plt.subplots(figsize=(6,6))

    # Draw triangle
    triangle = Polygon([[-1/np.sqrt(3),0], [0,1], [1/np.sqrt(3),0]], closed=True, edgecolor='black', fill=False, lw=2, zorder=10)
    ax.add_patch(triangle)

    # --- Bounds for background ---
    xp = np.linspace(0, 1, 1200)
    txp = (-2*xp + 1)/np.sqrt(3)
    n_samples = len(samples)
    alpha = 0.05
    chi2val = stats.chi2.ppf(1 - alpha, 1)
    c_add = 0.5
    # Extended bound (dashed)
    delta = np.sqrt(
        c_add**2 * xp*(1-xp)*(xp*(1-xp)-0.5)/(n_samples**2) +
        xp**2*(1-xp)**2*chi2val/n_samples
    )
    y_up = 2*xp*(1-xp) + 2*c_add*(1 - xp*(1-xp))/n_samples + 2*delta
    y_lo = 2*xp*(1-xp) - 2*c_add*(1 - xp*(1-xp))/n_samples - 2*delta
    y_hw = 2*xp*(1-xp)

    # FULL seamless background (covers triangle)
    fill_hwe_background(ax, txp, y_lo, y_up)

    # --- Points, colorbar ---
    scat = ax.scatter(tx, ty, s=21, c=color, cmap='plasma', marker='o', edgecolors='black', linewidth=0.11, alpha=1, zorder=3)
    vmin, vmax = np.min(c), np.max(c)
    tick_labels = pretty_log_ticks(vmin, vmax)
    tick_locs = np.log(tick_labels)
    cbar = plt.colorbar(scat, ax=ax, ticks=tick_locs, fraction=0.04, pad=0.06)
    cbar.ax.set_yticklabels([str(t) for t in tick_labels])
    cbar.set_label("SNP count")

    # HWE and bounds (all clipped)
    def clip_line_to_triangle(xarr, yarr):
        mask = xy_inside_triangle(xarr, yarr)
        return xarr[mask], yarr[mask]
    txpp, ypp = clip_line_to_triangle(txp, y_hw)
    ax.plot(txpp, ypp, "r-", label="HWE expectation", lw=2, zorder=12)
    ypplus = 2*xp*(1-xp) + 2*xp*(1-xp) * np.sqrt(chi2val / n_samples)
    ypminus = 2*xp*(1-xp) - 2*xp*(1-xp) * np.sqrt(chi2val / n_samples)
    ax.plot(*clip_line_to_triangle(txp, ypplus), "r-", lw=1, zorder=11)
    ax.plot(*clip_line_to_triangle(txp, ypminus), "r-", lw=1, zorder=11)
    ax.plot(*clip_line_to_triangle(txp, y_up), "r--", lw=1, zorder=11)
    ax.plot(*clip_line_to_triangle(txp, y_lo), "r--", lw=1, zorder=11)

    skip = 0.02
    labelsize = 17
    ax.annotate("AA", xy=(-1/np.sqrt(3), 0-skip), ha='right', va='top', fontsize=labelsize)
    ax.annotate("AB", xy=(0, 1+skip), ha='center', va='bottom', fontsize=labelsize)
    ax.annotate("BB", xy=(1/np.sqrt(3), 0-skip), ha='left', va='top', fontsize=labelsize)
    ax.set_aspect('equal')
    ax.axis('off')

    plt.title(f"Hardy-Weinberg ternary plot for {population_name}", fontsize=18, pad=20)
    plt.tight_layout()
    if output_file is not None:
        plt.savefig(output_file)
        print(f"[INFO] Saved plot to {output_file}")
    else:
        plt.show()

def main():
    parser = argparse.ArgumentParser(description="Draw a Hardy-Weinberg ternary plot for one population using a VCF and popmap. Green background shows 'inside bounds', red otherwise.")
    parser.add_argument("vcf", help="Input VCF file")
    parser.add_argument("popmap", help="Popmap file")
    parser.add_argument("population", help="Population name (as in popmap)")
    parser.add_argument("-o", "--output", help="Output file (default: interactive)", default=None)
    parser.add_argument("--double-ids", action="store_true", help="VCF contains doubled ids for samples (result of LD pruning using plink)")
    args = parser.parse_args()

    hwe_ternary_plot(
        vcf_file=args.vcf,
        popmap_file=args.popmap,
        population_name=args.population,
        output_file=args.output,
        double_ids=args.double_ids,
    )

    
if __name__=="__main__":
    main()
