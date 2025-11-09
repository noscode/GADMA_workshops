# GADMA Installation

During the workshop you will learn how to use GADMA for demographic inference.
We kindly ask you to install GADMA on your system using the instructions below.

## Platform

Choose your platform to get recommendations and installation instructions:

```{tab} Linux
GADMA is available for Linux system.
```

```{tab} Windows
GADMA is available for Windows, but we recommend using the [Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/install) (WSL) for the best experience.
If you are using WSL, please follow the instructions for Linux.
```

```{tab} MacOS
GADMA is available for MacOS system.
```

## Activate Conda Environment

```bash
conda activate gadma_workshop_env
```

## Installation

* Install specified version of `moments` (unfortunately, GADMA is not yet compatible with the most recent version):
    ```bash
    pip install moments-popgen==1.3.1
    ```

````{tab} Linux
* Install GADMA using `pip`:
    ```bash
    pip install gadma
    ```
````

````{tab} Windows
* Install GADMA using `pip`:
    ```bash
    pip install gadma
    ```
````

````{tab} MacOS
* Install `dadi` and `scikit-allel` using `conda` first:
    ```bash
    conda install dadi scikit-allel
    ```
* Install GADMA using `pip`:
    ```bash
    pip install gadma
    ```
````

## Check the version of `matplotlib`

We will use a specific version of matplotlib to avoid some warnings:
```bash
pip install "matplotlib<3.5"
```

## Verify Installation

1. To verify installation first run:
    ```bash
    gadma --test
    ```
    You should see the following output:
    ```text
    --Finish pipeline--

    --Test passed correctly--

    Thank you for using GADMA!

    In case of any questions or problems, please contact: ekaterina.e.noskova@gmail.com
    ```
    
2. Download example data [`example_input_for_gadma.sfs`](https://github.com/noscode/GADMA_workshops/raw/refs/heads/main/docs/source/2024_18_11/files/example_input_for_gadma.sfs) and input file [`gadma_params.sfs`](https://github.com/noscode/GADMA_workshops/raw/refs/heads/main/docs/source/2024_18_11/files/gadma_params):

    ``` bash
    wget https://github.com/noscode/GADMA_workshops/raw/refs/heads/main/docs/source/2024_18_11/files/example_input_for_gadma.sfs
    wget https://github.com/noscode/GADMA_workshops/raw/refs/heads/main/docs/source/2024_18_11/files/gadma_params
    ```
    And run:
    ```bash
    gadma -p gadma_params
    ```
    You should see the following output:
    ```text
    --Finish pipeline--
    ```

## Let Us Know You Were Successful
In order for us to understand how many participants are ready for the workshop, we ask you to send us some results of your run.

* Print **the following line** of the file `gadma_output/GADMA.log`:
    ```bash
    tail -25 gadma_output/GADMA.log | head -1 | xargs
    ```
* Please **send us** this line via the following form: <a class="btn btn-outline-primary btn-lg" href="https://forms.office.com/e/pHVbkRydwz" role="button">Send Your Result</a>


## Troubleshooting

If you have any problems with installation:

````{tab} Linux
* You can install GADMA using `conda`
    ```bash
    conda install gadma
    ```
* Take a look at the official [installation documentation](https://gadma.readthedocs.io/en/latest/user_manual/installation.html)
* If you still face issues, please write to [ekaterina.e.noskova@gmail.com](mailto:ekaterina.e.noskova@gmail.com).
````

````{tab} Windows
* You can install GADMA using `conda`
    ```bash
    conda install gadma
    ```
* Take a look at the official [installation documentation](https://gadma.readthedocs.io/en/latest/user_manual/installation.html)
* If you still face issues, please write to [ekaterina.e.noskova@gmail.com](mailto:ekaterina.e.noskova@gmail.com).
````

````{tab} MacOS
* You can install GADMA using `conda`
    ```bash
    conda install gadma
    ```
* If you faced an issue for `moments` (`moments-popgen`) package, try installing it independently using:
    ```bash
    pip install Cython
    pip install "setuptools_scm>=8"
    pip install --no-build-isolation moments-popgen
    ```
    Run GADMA installation after.
* Take a look at the official [installation documentation](https://gadma.readthedocs.io/en/latest/user_manual/installation.html)
* If you still face issues, please write to [ekaterina.e.noskova@gmail.com](mailto:ekaterina.e.noskova@gmail.com).
````
