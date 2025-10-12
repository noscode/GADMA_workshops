# Set Up Conda Environment

We recommend to create and set up an empty [conda environment](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#):
```console
$ conda create -n gadma_workshop_env python=3.10
$ conda activate gadma_workshop_env
```

Add channels that we are going to use for installations:
```console
$ conda config --add channels bioconda
$ conda config --add channels conda-forge
```

## BCFtools Installation

We will require `bcftools` that can be easily installed using conda:
```console
$ conda install bcftools
```
