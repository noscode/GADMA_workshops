import sys
import os
import shutil
import numpy as np
import subprocess
import math

def create_one_bootstrap_file(filename, input_vcf, chosen_regions):
    with open(filename, 'w') as fout:
        with open(input_vcf) as fin:
            for line in fin:
                if line.strip("#").startswith("contig=<ID="):
                    break
                fout.write(line)
        for ind, region in enumerate(chosen_regions):
            length = int(region.split("_")[-1]) - int(region.split("_")[-2])
            fout.write(f"##contig=<ID={region}.{ind},length={length}>\n")

        # copy the rest of # lines from VCF
        have_seen_contigs = False
        with open(input_vcf) as fin:
            for line in fin:
                if not line.startswith("#"):
                    break
                if line.strip("#").startswith("contig=<ID="):
                    have_seen_contigs = True
                    continue
                if have_seen_contigs:
                    fout.write(line)

        # Now we write each contig information
        for ind, region in enumerate(chosen_regions):
            new_region = f"{region}.{ind}"
            contig = "_".join(region.split("_")[:-2])
            startPos = int(region.split("_")[-2])
            endPos = int(region.split("_")[-1])
            with open(input_vcf) as fin:
                for line in fin:
                    if line.startswith("#"):
                        continue
                    pos = int(line.split()[1])
                    if line.split()[0] == contig and startPos <= pos < endPos:
                        new_line = line.split()
                        new_line[0] = new_region
                        fout.write("\t".join(new_line) + "\n")

def calculate_distance(recombination_rate, probability):
    """
    Calculate the physical distance required for a given recombination rate 
    and probability of recombination.

    Parameters:
    recombination_rate (float): The recombination rate (r) per base pair per generation (e.g., 1e-8 for humans).
    probability (float): The probability of at least one recombination event (P), typically between 0 and 1.

    Returns:
    float: The physical distance (in base pairs) for which the probability of at least one recombination event
           is equal to or greater than the specified probability.
    """
    
    # Ensure probability is between 0 and 1
    if not (0 < probability < 1):
        raise ValueError("Probability must be between 0 and 1.")
    
    # Calculate the expected number of recombination events (λ)
    # Rearrange the formula: P(at least one recombination) = 1 - e^(-λ)
    # and solve for λ: λ = -ln(1 - P)
    lambda_value = -math.log(1 - probability)
    
    # Calculate the physical distance using λ = r * L
    # So, L = λ / r
    distance = lambda_value / recombination_rate
    
    # Return the calculated physical distance (in base pairs)
    return distance

def create_bootstrap_files(input_vcf, popmap, recombination_rate, dirname, n_boots, easySFS_location, easySFS_options):
    distance = calculate_distance(recombination_rate, probability=0.5)
    
    # Load contigs names that are presented in our file
    contigs_lens_list = []
    contig2len = {}
    with open(input_vcf) as f:
        for line in f:
            if line.strip("#").startswith("contig=<ID="):
                contig2len[line.split("ID=")[1].split(",")[0]] = int(line.strip().split("length=")[1][:-1])
                continue
            if line.startswith("#"):
                continue
            contig = line.split()[0]
            length = contig2len[contig]
            if contig not in [x[0] for x in contigs_lens_list]:
                contigs_lens_list.append([contig, length])
                
    # split contigs into regions
    regions_list = []
    for contig, length in contigs_lens_list:
        curStart = 0
        curEnd = 0
        for i in range(int(length / distance) + 1):
            curEnd += int((i + 1) * distance)
            if i == int(length / distance):
                curEnd = length
            regions_list.append(f"{contig}_{curStart}_{curEnd}")
            curStart = curEnd
            
    print(f"Found {len(regions_list)} regions to perform bootstrap over")
    
    # Load populations
    pops = []
    with open(popmap) as f:
        for line in f:
            pop_name = line.strip().split()[1]
            if pop_name not in pops:
                pops.append(pop_name)

    for i in range(0, n_boots):
        # Perform bootstrap over contigs
        new_inds = np.random.choice(
            range(len(regions_list)),
            size=len(regions_list),
            replace=True
        )
        new_regions = [regions_list[ind] for ind in new_inds]
        max_num_size = len(str(n_boots))
        filename = os.path.join(dirname, str(i+1).zfill(max_num_size) + ".vcf")
        create_one_bootstrap_file(
            filename=filename,
            input_vcf=input_vcf,
            chosen_regions=new_regions
        )

        # Now we want to run easySFS with the same options and get_our dadi fs file
        easySFS_output = os.path.join(dirname, str(i+1).zfill(max_num_size))
        process = subprocess.Popen(f"{easySFS_location} -i {filename} -p {popmap} {easySFS_options} -o {easySFS_output}".split())
        process.wait()
        # Copy sfs file to our directory
        src = os.path.join(easySFS_output, "dadi", "-".join(pops) + ".sfs")
        dst = os.path.join(dirname, str(i+1).zfill(max_num_size) + ".sfs")
        shutil.copyfile(src, dst)
        # Remove easySFS output directory
        shutil.rmtree(easySFS_output)

if __name__ == "__main__":
    if len(sys.argv) != 8:
        print(f"Usage: {sys.argv[0]} <original_VCF> <popmap> <rec_rate> <output_dir> <n_boots> <easySFS_location> <easySFS_arguments>")
    else:
        create_bootstrap_files(
            input_vcf=sys.argv[1],
            popmap=sys.argv[2],
            recombination_rate=float(sys.argv[3]),
            dirname=sys.argv[4],
            n_boots=int(sys.argv[5]),
            easySFS_location=sys.argv[6],
            easySFS_options=sys.argv[7]
        )
