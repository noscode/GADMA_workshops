# ATLAS Installation

During the workshop you will learn how to use ATLAS to prepare your sequencing data for demographic inference.
We kindly ask you to install ATLAS on your system using the instructions below.

## Activate Conda Environment

```bash
conda activate gadma_workshop_env
```

## Platform

Choose your platform to get recommendations and installation instructions:
```{tab} Linux
On Linux computers, you should be able to install ATLAS witout any difficulties.
```

```{tab} Windows
On Windows computers, use the [Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/install). Follow instructions for **Linux** system below.
```

```{tab} MacOS
On Linux computers, you should be able to install ATLAS.
```


## Installation

Install ATLAS using `conda`:
```bash
conda install bioconda::atlas
```

## Verify Installation

1. To verify installation first run:
    ```console
    $ atlas simulate --chrLength 1000
    ```
    You should see the following output:
    ```text
    - ATLAS terminated successfully in 0 seconds!
    ```
    
2. Download example input file [`example_for_atlas.bam`](https://github.com/noscode/GADMA_workshops/raw/refs/heads/main/docs/source/2024_18_11/files/example_for_atlas.bam):

    ``` console
    $ wget https://github.com/noscode/GADMA_workshops/raw/refs/heads/main/docs/source/2024_18_11/files/example_for_atlas.bam
    ```
    And run:
    ```console
    $ atlas BAMDiagnostics --bam example_for_atlas.bam
    ```
    You should see the following output:
    ```text
    - ATLAS terminated successfully in 0 seconds!
    ```

## Let Us Know You Were Successful
In order for us to understand how many participants are ready for the workshop, we ask you to send us some results of your run.

* Print **the first three lines** of file `example_for_atlas_mappingQualityHistogram.txt`:
    ```console
    $ head -3 example_for_atlas_mappingQualityHistogram.txt
    ```
* Please **send us** these lines via the following form:

<a class="btn btn-outline-primary btn-lg" href="https://forms.office.com/e/c4ayJQsKVE" role="button">Send Your Result</a>


## Troubleshooting

If you encounter the following error about `libgfortran.so.3`:
```text
atlas: error while loading shared libraries: libgfortran.so.3: cannot open shared object file: No such file or directory
```
You may need to install an older version of `libgfortran`:
```bash
conda install conda-forge/label/cf201901::libgfortran
```

If you have any other problems with installation:
* Take a look at the official [installation documentation](https://atlaswiki.netlify.app/getting_started#installation-via-git)
* If you still face issues, please write to [ekaterina.e.noskova@gmail.com](mailto:ekaterina.e.noskova@gmail.com).
