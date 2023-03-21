import sys
import os

def fix_ped_file(ped_file):
    assert ped_file.strip().split(".")[-1] == "ped"
    new_ped_file = ".".join(ped_file.split(".")[:-1]) + "_fixed.ped"
    with open(ped_file) as fin:
        with open(new_ped_file, "w") as fout:
            for line in fin:
                new_line = line.split("\t")
                new_line[5] = "-9"
                fout.write("\t".join(new_line) + "\n")
            
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <ped_file>")
    else:
        fix_ped_file(sys.argv[1])
