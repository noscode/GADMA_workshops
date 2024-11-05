import msprime
import os

full_output = "fake_vcf.vcf"
open(full_output, "w").close()

for i in range(1000):
    demography = msprime.Demography()
    demography.add_population(name="A", initial_size=10_000)
    ts = msprime.sim_ancestry(
            samples={"A": 5},
            demography=demography,
            recombination_rate=1.5e-8,
            sequence_length=2000)

    mts = msprime.sim_mutations(ts, rate=1.25e-8)

    with open(f"output_{i}.vcf", "w") as f:
        mts.write_vcf(f, contig_id=f"{i+1}")

    pos = 0
    with open(f"output_{i}.vcf") as f:
        with open(full_output, "a") as g:
            for line in f:
                if line.startswith("#") and i > 0:
                    continue
                if not line.startswith("#"):
                    if pos == int(line.split()[1]):
                        continue
                    pos = int(line.split()[1])
                g.write(line)

    os.remove(f"output_{i}.vcf")
