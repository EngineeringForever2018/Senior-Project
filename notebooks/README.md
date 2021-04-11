# Notebooks

The goal of this subproject is to create a library of data analysis tools and to hold the experiments that were conducted during the project. There are also some document processing utilities within the library.

## Installation (Development)

Working with a virtual environment is recommended so that you can delete and recreate the environment as needed.

### Recommendation: Use Conda

Using anaconda will allow you to easily create new virtual environments and delete them as needed. It also comes with tools for working with jupyter notebooks, which is important if you want to read the notebooks in the develop and deliver subdirectories.

First install conda from https://www.anaconda.com/ and make sure conda is in your path or that you use an anaconda terminal.

To create a new environment for this project, you can run:

```
conda create -n avpd
```

You can then activate the environment with `conda activate avpd`. If you want to get rid of the environment, deactivate it with `conda deactivate` and run `conda env remove -n avpd`.

### Installing Dependencies

The requirements for this project are located in the `requirements` folder. `dev.txt` is for dependencies that are only for development (like testing) whereas `common.txt` is for dependencies that are needed to run the project in development or not. To install all of these requirements, you can run

```
pip install -U -r requirements.txt
```

If you only want requirements from a specific file, then you can run `pip install -U -r requirements/common.txt` and so on for each file.

If you wish to add dependencies, simply add them to `common.txt` or `dev.txt`, whichever is appropriate.

## Running

You can run all tests by executing `pytest` within the notebooks project (where this README is). You can decide whether to run the unit tests or the benchmarks by themselves by running `pytest tests` and `pytest benchmarks`, respectively.
