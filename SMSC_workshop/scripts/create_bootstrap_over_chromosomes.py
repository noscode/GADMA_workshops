import sys
import os
import shutil
import numpy as np
import subprocess

def create_one_bootstrap_file(filename, input_vcf, chosen_contigs_and_lens):
    with open(filename, 'w') as fout:
        with open(input_vcf) as fin:
            for line in fin:
                if line.startswith("##contig=<ID="):
                    break
                fout.write(line)
        for ind, (contig, length) in enumerate(chosen_contigs_and_lens):
            fout.write(f"##contig=<ID={contig}.{ind},length={length}>\n")

        have_seen_contigs = False
        with open(input_vcf) as fin:
            for line in fin:
                if not line.startswith("#"):
                    break
                if line.startswith("##contig=<ID="):
                    have_seen_contigs = True
                    continue
                if have_seen_contigs:
                    fout.write(line)

        # Now we write each contig information
        for ind, (contig, length) in enumerate(chosen_contigs_and_lens):
            new_contig = f"{contig}.{ind}"
            with open(input_vcf) as fin:
                for line in fin:
                    if line.startswith("#"):
                        continue
                    if line.split()[0] == contig:
                        new_line = line.split()
                        new_line[0] = new_contig
                        fout.write("\t".join(new_line) + "\n")


def create_bootstrap_files(input_vcf, popmap, dirname, n_boots, easySFS_location, easySFS_options):
    # Load contigs names that are presented in our file
    contigs_lens_list = []
    contig2len = {}
    with open(input_vcf) as f:
        for line in f:
            if line.startswith("##contig=<ID="):
                contig2len[line.split("ID=")[1].split(",")[0]] = int(line.strip().split("length=")[1][:-1])
                continue
            if line.startswith("#"):
                continue
            contig = line.split()[0]
            length = contig2len[contig]
            if contig not in [x[0] for x in contigs_lens_list]:
                contigs_lens_list.append([contig, length])
    # Load populations
    pops = []
    with open(popmap) as f:
        for line in f:
            pop_name = line.strip().split()[1]
            if pop_name not in pops:
                pops.append(pop_name)

    for i in range(20, n_boots):
        # Perform bootstrap over contigs
        new_inds = np.random.choice(
            range(len(contigs_lens_list)),
            size=len(contigs_lens_list),
            replace=True
        )
        new_contigs = [contigs_lens_list[ind] for ind in new_inds]
        max_num_size = len(str(n_boots))
        filename = os.path.join(dirname, str(i+1).zfill(max_num_size) + ".vcf")
        create_one_bootstrap_file(
            filename=filename,
            input_vcf=input_vcf,
            chosen_contigs_and_lens=new_contigs
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
    if len(sys.argv) != 7:
        print(f"Usage: {sys.argv[0]} <original_VCF> <popmap> <output_dir> <n_boots> <easySFS_location> <easySFS_arguments>")
    else:
        create_bootstrap_files(
            input_vcf=sys.argv[1],
            popmap=sys.argv[2],
            dirname=sys.argv[3],
            n_boots=int(sys.argv[4]),
            easySFS_location=sys.argv[5],
            easySFS_options=sys.argv[6]
        )
