# Data Preparation

Below are the requirements and instructions to ensure your data is ready for analysis.

You will need the following:
* A file assigning each sample name to a population (see instructions below)
* A VCF file (see instructions below)
* Mutation rate (per bp per generation) for your species
* Length of sequence covered by your data 

## Example Dataset

If you do not have your data you can download the example dataset from [here](https://drive.google.com/drive/folders/1ZBT9aJxs-OUmzpsAj0BHflXgBK1FRpK6?usp=sharing).

This dataset includes genetic data for two populations of orangutans. The VCF file `chr1.vcf.gz` contains SNPs only for chromosome 1, which has a length of 227,913,704 base pairs. The popmap file (`popmap.txt`) provides the population assignments for each sample. Two populations are present: Bornean and Sumatran, with 10 samples each. The mutation rate is equal to 1.5 × 10⁻⁸ per base pair per generation.

**If you are using the example dataset provided for the workshop, you’re all set! You do not need to follow the steps below. Instead, please [let us know you were successful](#let-us-know-you-were-successful) by visiting the feedback section at the end of this page.**

## File with Population Assignments (`popmap.txt`)

For the workshop, you will need a file listing which population each of your samples belongs to.
Please create a plain text file called `popmap.txt` with two columns, separated by a tab, like this:

```
sample1    PopulationA
sample2    PopulationA
sample3    PopulationB
sample4    PopulationB
```

The first column is the sample name (must match the sample names used in your VCF file).
The second column is the population name (choose any labels you wish, e.g. "Pop1" or real population names).


```{tip}
If you have many samples and want to generate a list of them from your VCF, use the following command:

    bcftools query -l your_file.vcf

or

    bcftools query -l your_file.vcf.gz

This will print one sample name per line, which you can copy and paste into your popmap.txt and then add the corresponding population names.
```

```{note}
   It is absolutely fine if some samples in your VCF are not listed in your `popmap.txt`—they will simply be ignored in downstream analyses that require population assignments.
```


## VCF Preparation Instructions
Follow the instructions below to prepare VCF file.
Your final output should be a VCF file (`.vcf` or `.vcf.gz`) containing only high-quality, UNfiltered-for-MAF, single-nucleotide variants and indels.

We recommend extracting one chromosome to a separate VCF file and preparing it for the workshop.
This way, you can easily experiment with the smaller VCF during the workshop, and then run the full pipeline on your complete dataset.

To extract a single chromosome from your data:
````{tab} .vcf
```bash
bcftools view -r 'chromosome_name' full.vcf -Ov -o chr1.vcf
```
````

````{tab} .vcf.gz
```bash
bcftools index resolved.vcf.gz
bcftools view -r 'chromosome_name' full.vcf.gz -Ov -o chr1.vcf
```
````

```{note}
Make sure your conda environment is activated before running `bcftools`.

    conda activate gadma_workshop_env
```

1. **Start with your VCF file and exclude regions affected by selection (e.g. sex chromosomes)**

   To exclude sex chromosomes `X` and `Y` from your VCF file:
   ````{tab} .vcf
   ```bash
   bcftools view -t '^X,^Y' input.vcf -Ov -o autosomes.vcf
   ```
   ````

   ````{tab} .vcf.gz
   ```bash
   bcftools view -t '^X,^Y' input.vcf.gz -Oz -o autosomes.vcf.gz
   ```
   ````

2. **Ensure the VCF has passed standard variant quality filtering for SNP calling** 

   Do not apply any minor allele frequency (MAF) filtering—your file should retain both common and rare variants.
   Use the following command to select only high-quality variants (you can add `-f PASS` to filter for variants with `FILTER=PASS`):
   ````{tab} .vcf
   ```bash
   bcftools view -i 'QUAL>30 && INFO/DP>10' autosomes.vcf -Ov -o highqual.vcf
   ```
   ````

   ````{tab} .vcf.gz
   ```bash
   bcftools view -i 'QUAL>30 && INFO/DP>10' autosomes.vcf.gz -Oz -o highqual.vcf.gz
   ```
   ````

3. **Decompose multiallelic sites and resolve multi-nucleotide variants (MNVs):**
   ````{tab} .vcf
   ```bash
   bcftools norm -m -any highqual.vcf -Ov -o decomposed.vcf
   ```
   Check for any remaining unresolved complex MNVs. Run to get number `M` of positions with unresolved MNVs:
   ```bash
   awk '(length($4) > 1 || length($5) > 1) {print $1 "\t" $2}' decomposed.vcf | sort | uniq | wc -l
   ```
   Get the total number `N` of unique variants in current file (it should be >0):
   ```bash
   awk '(length($4) > 1 || length($5) > 1) {print $1 "\t" $2}' decomposed.vcf | sort | uniq | wc -l
   ```
   If `M=0` you can skip the next step.
   ````

   ````{tab} .vcf.gz
   ```bash
   bcftools norm -m -any highqual.vcf.gz -Oz -o decomposed.vcf.gz
   ```
   Check for any remaining unresolved complex MNVs. Run to get number `M` of positions with unresolved MNVs:
   ```bash
   bcftools view -H decomposed.vcf.gz | awk '(length($4) > 1 || length($5) > 1) {print $1 "\t" $2}' | sort | uniq | wc -l
   ```
   Get the total number `N` of unique variants in current file (it should be >0):
   ```bash
   bcftools view -H your.vcf.gz | awk '(length($4) > 1 || length($5) > 1) {print $1 "\t" $2}' | sort | uniq | wc -l
   ```
   If `M=0` you can skip the next step.
   ````

4. **Remove or resolve the remaining multi-nucleotide variants:**
   If `M` > 0, you can either:
   - Remove multi-nucleotide variants completely (although you loose some data):
      ````{tab} .vcf
      ```bash
      bcftools view -i '((strlen(REF)==1 && strlen(ALT)==1) || (strlen(REF)!=strlen(ALT) && strlen(REF)<=1 && strlen(ALT)<=1))' decomposed.vcf -Ov -o no_mn_indels.vcf
      ```
      ````

      ````{tab} .vcf.gz
      ```bash
      bcftools view -i '((strlen(REF)==1 && strlen(ALT)==1) || (strlen(REF)!=strlen(ALT) && strlen(REF)<=1 && strlen(ALT)<=1))' decomposed.vcf.gz -Oz -o resolved.vcf.gz
      ```
      ````

      ```{important}
      Do not forget to correct your sequence length by (1 - `M`/`N`), because you have removed ~`M`/`N` fraction of your data.
      ```


   - Or, left-align and normalize using bcftools and reference (⚠️ This step requires a reference genome FASTA file (`reference.fa`) that matches the one used for your SNP calling):
      ````{tab} .vcf
      ```bash
      bcftools norm -m -any -f reference.fa decomposed.vcf -Ov -o no_mn_indels.vcf
      ```
      ````

      ````{tab} .vcf.gz
      ```bash
      bcftools norm -m -any -f reference.fa decomposed.vcf.gz -Oz -o resolved.vcf.gz
      ```
      ````

5. **After resolving, repeat the check to ensure all variants are now only SNVs/indels:**

   ````{tab} .vcf
   ```bash
   awk '{if($0 !~ /^#/ && length($4)>1 && length($5)>1 && length($4)==length($5)) print $0}' resolved.vcf
   ```
   ````

   ````{tab} .vcf.gz
   ```bash
   bcftools view -H resolved.vcf.gz | awk '{if(length($4)>1 && length($5)>1 && length($4)==length($5)) print $0}'
   ```
   ````

   - If no lines are printed, your file is ready.


Your VCF file is ready, good job!


## Let Us Know You Were Successful
In order for us to understand how many participants are ready for the workshop, we ask you to send us feedback that your data is ready.

* Please run the following command for your `chr1.vcf`:
   ````{tab} .vcf
   ```bash
   awk '{if(length($4)!=1 || length($5)!=1 || $5 ~ /,/) print $0}' your_final.vcf | wc -l
   ```
   ````

   ````{tab} .vcf.gz
   ```bash
   bcftools view -H your_final.vcf.gz | awk '{if(length($4)!=1 || length($5)!=1 || $5 ~ /,/) print $0}' | wc -l
   ```
   ````

* Please **send us** the output via the following form: <a class="btn btn-outline-primary btn-lg" href="https://forms.office.com/e/ZNxawfHtFt" role="button">Send Your Result</a>
