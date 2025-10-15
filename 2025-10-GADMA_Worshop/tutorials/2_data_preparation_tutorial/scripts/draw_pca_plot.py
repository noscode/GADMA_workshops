import os
from matplotlib import pyplot as plt
from sklearn.decomposition import PCA
import numpy as np

def read_popmap(popmap_filename):
    pop2ind = {}
    sample2pop = {}
    with open(popmap_filename) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            sample, pop = line.split()
            if pop not in pop2ind:
                pop2ind[pop] = len(pop2ind)
            sample2pop[sample] = pop
    return pop2ind, sample2pop

def read_vectors_from_vcf(vcf_filename, samples, only_full_data=False, double_ids=True):
    array = []
    sample_names = []
    with open(vcf_filename) as f:
        for line in f:
            if line.startswith("#") and not line.startswith("##"):
                fields = line.strip().split()
                all_sample_names = fields[9:]
                if double_ids:
                    sample_names = [name.split("_")[0] for name in all_sample_names if name.split("_")[0] in samples]
                    sample_indices = [9 + i for i in range(len(all_sample_names)) if all_sample_names[i].split("_")[0] in samples]
                else:
                    sample_names = [name for name in all_sample_names if name in samples]
                    sample_indices = [9 + i for i in range(len(all_sample_names)) if all_sample_names[i] in samples]
                if (len(sample_names) == 0):
                    raise ValueError("No samples from popmap file are presented in VCF. Check the labels in both files and make sure argument `double-ids` is set correctly.")
            if line.startswith("#"):
                continue
            line_has_missing_info = False
            all_missing = True
            spl_line = line.strip().split()
            genotypes = [spl_line[i] for i in sample_indices]
            values = []
            for genotype in genotypes:
                if genotype[0] == "." or genotype[2] == ".":
                    line_has_missing_info = True
                    values.append(np.nan)
                else:
                    all_missing = False
                    values.append(int(genotype[0]) + int(genotype[2]))
            if all_missing:
                continue
            if only_full_data and line_has_missing_info:
                continue
            values = np.array(values, dtype=float)
            if line_has_missing_info:
                values[np.isnan(values)] = np.nanmean(values)
            array.append(values)
    if len(array) == 0:
        raise ValueError("No variants were read from the VCF file.")
    array = np.swapaxes(np.array(array), 0, 1)
    return sample_names, array

def pca_plot(
    vcf_file,
    popmap_file,
    output_file=None,
    title="PCA Plot",
    fig_size=(7,5),
    only_full_data=False,
    double_ids=True,
    show_sample_names=False,
):
    """
    Create a PCA plot from a VCF file and a popmap file.

    If output_file is specified, saves the plot to that file.
    If output_file is None or empty, shows the plot interactively.
    """

    for filename in [vcf_file, popmap_file]:
        if not os.path.exists(filename):
            raise FileNotFoundError(f"File not found: {filename}")

    # Read popmap
    print("[INFO] Reading popmap...")
    pop2ind, sample2pop = read_popmap(popmap_file)
    print(f"[INFO] {len(sample2pop)} samples, {len(pop2ind)} populations detected")

    # Read VCF
    print("[INFO] Reading VCF (this might take a while)...")
    sample_names, array = read_vectors_from_vcf(vcf_file, sample2pop.keys(), only_full_data, double_ids)
    print(f"[INFO] Data shape after filtering: {array.shape}")

    # Perform PCA
    print("[INFO] Running PCA...")
    if len(array.shape) != 2 or array.shape[0] < 2:
        raise ValueError("Not enough data to run PCA!")
    pca = PCA(n_components=2)
    X_transformed = pca.fit_transform(array)

    # Plot
    action = "Displaying" if not output_file else f"Saving to {output_file}"
    print(f"[INFO] {action} ...")
    cmap = plt.get_cmap("tab10")
    plt.figure(figsize=fig_size)
    used_labels = set()
    for sample_name, x in zip(sample_names, X_transformed):
        pop = sample2pop[sample_name]
        i = pop2ind[pop]
        label = pop
        show_label = label not in used_labels
        plt.plot([x[0]], [x[1]], marker="o", color=cmap(i), alpha=0.65, label=label if show_label else None)
        used_labels.add(label)
        if show_sample_names:
            plt.text(x[0]+0.02, x[1]+0.02, sample_name, fontsize=7, alpha=0.8)
    plt.xlabel("PCA 1")
    plt.ylabel("PCA 2")
    plt.title(title)
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=8)
    plt.tight_layout()
    if output_file:
        plt.savefig(output_file)
        plt.close()
    else:
        plt.show()
    print("[INFO] Done.")

# Optional CLI usage
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Draw PCA plot from VCF and popmap files.")
    parser.add_argument("vcf", help="VCF filename")
    parser.add_argument("popmap", help="Popmap filename (tab-separated: sample pop)")
    parser.add_argument("output", nargs='?', default=None, help="Output file for the plot (e.g., pca.png); if omitted, plot will be shown interactively")
    parser.add_argument("--full", action="store_true", help="Use only full data rows (exclude missing genotypes)")
    parser.add_argument("--show-sample-names", action="store_true", help="Display sample names on the plot at each point")
    parser.add_argument("--double-ids", action="store_true", help="VCF contains doubled ids for samples (result of LD pruning using plink)")
    args = parser.parse_args()

    pca_plot(
        vcf_file=args.vcf,
        popmap_file=args.popmap,
        output_file=args.output,
        only_full_data=args.full,
        double_ids=args.double_ids,
        show_sample_names=args.show_sample_names
    )
