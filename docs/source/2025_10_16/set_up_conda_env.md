# Set Up Conda Environment

## Platform
Choose your platform to get recommendations:

````{tab} Linux
You should be able to install everything on Linux systems.
````

````{tab} Windows
We recommend using the [Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/install) (WSL) for the best experience.
If you are using WSL, please follow the instructions for Linux.
````

````{tab} MacOS
You should be able to install everything on MacOS systems.
```{note}
All installation commands are intended for the Bash shell, which is the default on most macOS systems. If you use a different shell (like zsh), they should still work, but let us know if you have issues.
```
````
## Set Up Conda Environment

We recommend to create and set up an empty [conda environment](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#):
```bash
conda create -n gadma_workshop_env python=3.10
conda activate gadma_workshop_env
```

Add channels that we are going to use for installations:
```bash
conda config --add channels bioconda
conda config --add channels conda-forge
```

## BCFtools Installation

We will require `bcftools` that can be easily installed using conda:
```bash
conda install bcftools
```
