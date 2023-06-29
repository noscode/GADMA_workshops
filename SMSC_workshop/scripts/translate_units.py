import sys
import os

def translate_units(input_file, output_file, theta0):
    with open(input_file) as fin:
        header = next(fin)
        params = ["Nanc"]
        params.extend(header.split(",")[1:-1])
        with open(output_file, 'w') as fout:
            fout.write("," + ",".join(params) + "\n")
            for line in fin:
                new_vals = [line.split(",")[0]]
                Nanc = float(line.split(",")[-1]) / theta0
                new_vals.append(Nanc)
                for par, val in zip(params, line.split(",")[1:-1]):
                    if par.startswith("n"):
                        new_vals.append(float(val) * Nanc)
                    elif par.startswith("t"):
                        new_vals.append(float(val) * 2 * Nanc)
                    elif par.startswith("m"):
                        new_vals.append(float(val) / (2 *  Nanc))
                    else:
                        new_vals.append(float(val))
                fout.write(",".join([str(x) for x in new_vals]) + "\n")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <input_file.csv> <theta0>")
    else:
        assert sys.argv[1].split(".")[-1] == "csv"
        output_file = ".".join(sys.argv[1].split(".")[:-1]) + "_translated.csv"
        translate_units(input_file=sys.argv[1], output_file=output_file, theta0=float(sys.argv[2]))
