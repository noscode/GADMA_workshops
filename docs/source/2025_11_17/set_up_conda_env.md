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

## Optional: Install Jupyter Notebook

During the workshop, we will be demonstrating several Jupyter Notebooks.

**You are not required to install anything** for the workshop itself. All notebooks will be accessible for you to view **online**—so you can follow along without installing any software.

However, if you’d like to **run the notebooks on your own laptop** after the workshop or experiment with them interactively, you will need to install Jupyter Notebook.

**What is Jupyter Notebook?** Jupyter Notebook is an application that lets you create and share interactive documents, which can include live code, plots, images, and explanations—all in one place.
When you launch Jupyter Notebook, it opens in your web browser and acts as an interactive workspace for programming, exploring data, and visualizing results. Learn more: [here](https://jupyter-notebook.readthedocs.io/en/latest/).

To install Jupyter Notebook:
```bash
conda install notebook
```

Once installation finishes, navigate to the folder where you have saved the notebooks I will provide during the workshop. Then start Jupyter Notebook with:
```bash
jupyter notebook
```
This will open the Jupyter interface in your default web browser, showing all notebooks in your current folder.
