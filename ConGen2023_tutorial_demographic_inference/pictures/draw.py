import dadi
from matplotlib import pyplot as plt
import matplotlib
import moments
import os

matplotlib.rc("font", size=20)


fs = dadi.Spectrum.from_file("YRI_CEU.fs")
#fs = dadi.Spectrum.from_file("sfs_52.fs")
fs = fs.marginalize([1])
fs.pop_ids = ["YRI"]
#fs.pop_ids = ["Black-footed ferret"]

cm = plt.cm.get_cmap('hsv')

figsize=(6,5)
plt.figure(figsize=figsize)
fig, ax = plt.subplots()
n, bins, patches = plt.hist([i-1.5 for i in range(1, len(fs))], weights=fs[1:], bins=len(fs)-1)

print(fs)
print(n)
print(bins)

col = (n-1)/(1e4-1)
#col = (n-1)/(40000-1)
for c, p in zip(col, patches):
    plt.setp(p, 'facecolor', cm(c))

ticks = [(bins[i] + bins[i+1]) / 2 for i in range(len(bins) - 1)]
ticks.append(ticks[-1] + 0.95)
plt.xticks(ticks[:22:5], labels=[f"{i}" for i in range(len(fs))][:22:5])
plt.margins(x=0)
#plt.yscale("log")
plt.xlabel("Allele frequency", fontsize=25)
plt.ylabel("Count", fontsize=25)
# We change the fontsize of minor ticks label
ax.tick_params(axis='both', which='major', labelsize=20)
ax.tick_params(axis='both', which='minor', labelsize=20)
plt.tight_layout()
#plt.savefig("1d_plot_bff.svg")
plt.savefig("1d_plot.png")
os.exit(0)

plt.figure(figsize=figsize)
matplotlib.rc("font", size=25)
fs = dadi.Spectrum.from_file("YRI_CEU.fs")
dadi.Plotting.plot_single_2d_sfs(fs, vmin=1, vmax=None, ax=None, 
                       pop_ids=["YRI", "CEU"], extend='neither', colorbar=True,
                       cmap=plt.get_cmap("hsv"))
plt.xticks(fontsize=20)
plt.tight_layout()
plt.savefig("2d_plot.png")

plt.figure(figsize=figsize)
fs = dadi.Spectrum.from_file("YRI.CEU.CHB.fs")
dadi.Plotting.plot_3d_spectrum(fs, fignum=3, vmin=1, vmax=None, pop_ids=["YRI", "CEU", "CHB"],
                     show=False)
plt.tight_layout()
plt.savefig("3d_plot.png")
plt.show()
