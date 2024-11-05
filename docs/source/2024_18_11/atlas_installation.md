# ATLAS Installation

During the workshop you will learn how to use ATLAS to prepare your sequencing data for demographic inference.
We kindly ask you to install ATLAS on your system using the instructions below.

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

## Dependencies

We will start with installation of ATLAS dependencies:

````{tab} Linux
* Check that `gcc` compiler of **version 9 or higher** is installed:
    ```console
    $ gcc --version
    ```
    If not, please install `gcc`:
    ```console
    $ sudo apt install gcc
    ```
* Check that `cmake` of **version 3.14 or higher** is installed:
    ```console
    $ cmake --version
    ```
    If not, please install `cmake`:
    ```console
    $ sudo apt install cmake
    ```
````

````{tab} MacOS
* Check that `clang` compiler is installed:
    ```console
    $ clang --version
    ```
* Install `samtools`, `cmake`, `autoconf` and `automake`:
    ```console
    $ brew install samtools cmake autoconf automake
    ```
````


## Installation

Download ATLAS repository:

```console
$ git clone --depth 1 https://bitbucket.org/WegmannLab/atlas.git
```

And run compilation:
```console
$ cd atlas
$ mkdir -p build
$ cd build
$ cmake ..
$ make
```

You can add the path to atlas as an alias in your `.bashrc` file as follows to avoid having to indicate the path to atlas/build all the time:
```bash
alias atlas='/path/to/atlas/build/atlas'
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

<a class="btn btn-outline-primary btn-lg" href="https://forms.gle/tFasZBhbvHzmk2yR7" role="button">Send Your Result</a>


## Troubleshooting

If you have any problems with installation:

````{tab} Linux
* You can install ATLAS using `conda`
    ```console
    $ conda env create -f conda.yml
    $ conda activate atlas 
    $ mkdir build; cd build
    ```
    As `cmake` and `conda` do not play together nicely, you need to tell cmake where conda puts its binnaries and libraries:
    ```console
    $ cmake .. -GNinja -DCONDA=ON -DCMAKE_C_COMPILER=$(which gcc) -DCMAKE_CXX_COMPILER=$(which g++) -DCMAKE_LIBRARY_PATH=$CONDA_PREFIX/lib -DCMAKE_INCLUDE_PATH=$CONDA_PREFIX/include
    $ ninja
    ```
* Take a look at the official [installation documentation](https://atlaswiki.netlify.app/getting_started#installation-via-git)
* If you still face issues, please write to [ekaterina.e.noskova@gmail.com](mailto:ekaterina.e.noskova@gmail.com).
````

````{tab} MacOS
* Try using `gcc` compiler instead of `clang` for compilation.
* You can install ATLAS using `conda`
    ```console
    $ conda env create -f conda.yml
    $ conda activate atlas 
    $ mkdir build; cd build
    ```
    As `cmake` and `conda` do not play together nicely, you need to tell cmake where conda puts its binnaries and libraries:
    ```console
    $ cmake .. -GNinja -DCONDA=ON -DCMAKE_C_COMPILER=$(which gcc) -DCMAKE_CXX_COMPILER=$(which g++) -DCMAKE_LIBRARY_PATH=$CONDA_PREFIX/lib -DCMAKE_INCLUDE_PATH=$CONDA_PREFIX/include
    $ ninja
    ```
* Take a look at the official [installation documentation](https://atlaswiki.netlify.app/getting_started#installation-via-git)
* If you still face issues, please write to [ekaterina.e.noskova@gmail.com](mailto:ekaterina.e.noskova@gmail.com).
````
