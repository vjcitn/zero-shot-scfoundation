# ABOUT THIS FORK

The notebook for geneformer won't run out of the box.  The envs/conda-env.yml needed a few
extra entries.  A full session_info result is at the end of this README.



# THE FOLLOWING IS THE ORIGINAL README

# Foundation models in single-cell biology: evaluating zero-shot capabilities

[![DOI](https://badgen.net/badge/DOI/10.1101%2F2023.10.16.561085/red)](https://www.biorxiv.org/content/10.1101/2023.10.16.561085) [![DOI](https://badgen.net/badge/figshare/10.6084%2Fm9.figshare.24747228/green)](https://doi.org/10.6084/m9.figshare.24747228)

This repository contains the code that accompanies our paper, **Assessing the limits of zero-shot foundation models in single-cell biology**. You can find the preprint of the paper [here](https://www.biorxiv.org/content/10.1101/2023.10.16.561085).


## Project overview

In this project, we assess two proposed foundation models in the context of single-cell RNA-seq: Geneformer ([pub](https://www.nature.com/articles/s41586-023-06139-9), [code](https://huggingface.co/ctheodoris/Geneformer)) and scGPT ([pub](https://www.biorxiv.org/content/10.1101/2023.04.30.538439v2), [code](https://github.com/bowang-lab/scGPT)). We focus on evaluating the zero-shot capabilities of these models, specifically their ability to generalize beyond their original training objectives. Our evaluation targets two main tasks: cell type clustering and batch integration. In these tasks, we compare the performance of Geneformer and scGPT against two baselines: scVI  ([pub](https://www.nature.com/articles/s41592-018-0229-2), [code](https://docs.scvi-tools.org/en/stable/user_guide/models/scvi.html)) and a heuristic method that selects highly variable genes (HVGs). We also investigate the performence of the models in reconstructing the gene expression profiles of cells, and compare it against the baselines - such as a mean expression value or average ranking.

## Dependencies

Currently the code requires the GPUs supported by flash attention, required for scGPT to run.

GPUs supported by flash attention are:
- Ampere, Ada, or Hopper GPUs (e.g., A100, RTX 3090, RTX 4090, H100).
- Turing GPUs (T4, RTX 2080)

## Installation

The amount of time that the installation takes depends on (1) whether you chose mamba over conda (former is much faster in my experience), (2) how many dependencies are already present in your environment, (3) the speed of your internet connection, and (4) the speed of your machine. The following steps, took me about 1 hour to complete on a remote HPC with fast internet connection.

### Conda / Mamba

You can install the dependencies using conda. To do so, you need to have conda installed on your machine. If you don't have it, you can install it from [here](https://docs.conda.io/en/latest/miniconda.html).

We strongly recommend using [mamba](https://mamba.readthedocs.io/en/latest/user_guide/mamba.html) instead of conda, since it is much faster in our experience. If you are starting from scratch, i.e. don't have conda installed, you can install mamba instead of conda by following their guide [here](https://mamba.readthedocs.io/en/latest/mamba-installation.html#fresh-install-recommended).

If you already have conda install and want to benefit from the speed and enhanced experience of mamba, you can do so by running:

```bash
# install mamba in your base environment
conda install -c conda-forge mamba
```

Be warned though, this is not a recommended way by the creators of mamba.

*Note:* If you installed mamba from scratch, in all commands below you can replace `conda` with `mamba`. However, if you just installed mamba in your existing conda install use `mamba` only for creating the environment.

#### 1. Installing conda environment

```bash
# install conda environment from conda_env.yml file
# in this step, you can use mamba instead of conda for speed
conda env create -f envs/conda_env.yml
```

To activate the environment, run:

```bash
# activate conda environment
conda activate sc_foundation_evals
```

#### 2. Installing scGPT

This can be tricky, as scGPT requires specific flash-attn version, and flash attention can be difficult to install. If you get any issues with installation, check out the instructions from the flash-attn authors [here](https://github.com/Dao-AILab/flash-attention#installation-and-features), but bear in mind that they have significantly updated their code with 2.0 release, so the instructions might not entirely work for this version.

```bash
# make sure sc_foundation_evals env is activated
# We have found it easier to install flash attention first, and then scGPT
pip install flash-attn==11.0.4 --no-build-isolation
# then install v1.0.6 version of scGPT
pip install git+https://github.com/bowang-lab/scGPT.git@v0.1.6
pip install wandb
```

#### 3. Installing Geneformer

```bash
pip install git+https://huggingface.co/ctheodoris/Geneformer.git

```

#### 4. Installing `sc_foundation_evals` package

And finally, install the `sc_foundation_evals` package (the code to run evaluations on zero-shot scFoundation models) itself.

```bash
cd sc_foundation_evals
pip install .
```

To run notebooks you also need to have the weights of the models downloaded. scGPT weights are avaialble [here](https://github.com/bowang-lab/scGPT#pretrained-scgpt-model-zoo) and Geneformer weights are available in its repository. As per the instructions in the Geneformer repository, make sure you have `git lfs` installed before downloading the weights via repository cloning.


```bash 
# Make sure you have git-lfs installed (https://git-lfs.com)
git lfs install
git clone https://huggingface.co/ctheodoris/Geneformer
```

### Docker

Support for docker is coming soon.

## Running the code

### Copying this repository

To run the code, you need to clone this repository.

```bash
git clone https://github.com/microsoft/zero-shot-scfoundation
```

And download and unpack the data, stored at figshare (see [here](https://doi.org/10.6084/m9.figshare.24747228) for more details).

```bash
cd zero-shot-scfoundation
# download and unpack the data
wget https://figshare.com/ndownloader/files/43480497 -O data.zip
unzip data.zip && rm data.zip
```

### Notebooks

To best understand the code and it's organization, please have a look at the notebooks. The `notebooks` directory currently contains the following notebooks:

- [scGPT_zero_shot](notebooks/scGPT_zero_shot.ipynb) - notebook for running scGPT zero-shot evaluation
- [Geneformer_zero_shot](notebooks/Geneformer_zero_shot.ipynb) - notebook for running Geneformer zero-shot evaluation
- [Baselines_HVG_and_scVI](notebooks/Baselines_HVG_and_scVI.ipynb) - notebook for running the baselines used in the paper, i.e. HVG and scVI.


## Any questions?

If you have any questions, or find any issues with the code, please open an issue in this repository. You can find more information on how to file an issue in [here](/SUPPORT.md). We also welcome any contributions to the code - be sure to checkout the **Contributing** section below.

## Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.opensource.microsoft.com.

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft 
trademarks or logos is subject to and must follow 
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third-party trademarks or logos are subject to those third-party's policies.

# FULL SESSION_INFO

NA implies whatever mamba/pip could get on 23 june 2024 with the envs set
according to envs/conda_env.yml (as revised in this fork), with the addition
of 

Geneformer (from https://huggingface.co/ctheodoris/Geneformer)
```
commit ead055038810da74c68e1c15ad8a8282a26c0943
```

and 

https://github.com/vjcitn/zero-shot-scfoundation commits of june 23 2024

```
----
Session information updated at 2024-06-23 15:42
>>> session_info.main()

>>> session_info.show(dependencies=True)
-----
sc_foundation_evals NA
session_info        1.0.0
-----
IPython                     8.25.0
PIL                         9.4.0
PyComplexHeatmap            1.7.4
accumulation_tree           NA
aiohttp                     3.9.5
aiosignal                   1.3.1
anndata                     0.10.8
asttokens                   NA
async_timeout               4.0.3
attr                        23.2.0
brotli                      1.1.0
certifi                     2024.06.02
cffi                        1.16.0
charset_normalizer          3.3.2
colorama                    0.4.6
colorlog                    NA
contourpy                   1.2.1
cycler                      0.12.1
cython_runtime              NA
datasets                    2.20.0
dateutil                    2.9.0
decorator                   5.1.1
deprecated                  1.2.14
dill                        0.3.8
exceptiongroup              1.2.0
executing                   2.0.1
filelock                    3.15.4
frozenlist                  1.4.1
fsspec                      2024.5.0
geneformer                  NA
google                      NA
h5py                        3.11.0
huggingface_hub             0.23.4
idna                        3.7
igraph                      0.10.3
jedi                        0.19.1
joblib                      1.4.2
kiwisolver                  1.4.5
leidenalg                   0.9.1
llvmlite                    0.42.0
loompy                      3.0.7
matplotlib                  3.7.5
mpl_toolkits                NA
mpmath                      1.3.0
multidict                   6.0.5
multiprocess                0.70.16
natsort                     8.4.0
networkx                    3.3
numba                       0.59.1
numpy                       1.26.4
numpy_groupies              0.11.1
packaging                   24.1
palettable                  3.3.3
pandas                      2.2.2
parso                       0.8.4
patsy                       0.5.6
prompt_toolkit              3.0.47
pure_eval                   0.2.2
pyarrow                     16.1.0
pyarrow_hotfix              NA
pycparser                   2.22
pydot                       2.0.0
pygments                    2.18.0
pyparsing                   3.1.2
pytz                        2024.1
pyudorandom                 1.0.0
requests                    2.32.3
safetensors                 0.4.3
scanpy                      1.9.8
scgpt                       0.2.1
scib                        1.1.5
scipy                       1.13.1
seaborn                     0.13.2
sitecustomize               NA
six                         1.16.0
sklearn                     1.5.0
socks                       1.7.1
stack_data                  0.6.3
statsmodels                 0.14.2
sympy                       1.12.1
tdigest                     0.5.2.1
texttable                   1.7.0
threadpoolctl               3.5.0
tokenizers                  0.19.1
torch                       2.1.2+cu121
torchdata                   0.7.1
torchgen                    NA
torchtext                   0.16.2+cpu
tqdm                        4.66.4
traitlets                   5.14.3
transformers                4.41.2
typing_extensions           NA
urllib3                     2.2.2
wcwidth                     0.2.13
wrapt                       1.16.0
xalt_python_pkg_filter      NA
xxhash                      NA
yaml                        6.0.1
yarl                        1.9.4
zoneinfo                    NA
-----
Python 3.10.14 | packaged by conda-forge | (main, Mar 20 2024, 12:45:18) [GCC 12.3.0]
Linux-6.5.0-41-generic-x86_64-with-glibc2.35
-----
Session information updated at 2024-06-23 15:43
```

