# Introduction

dSPP (or DSPP) stands for database for structural propensity of proteins.
It is a first database that's aiming to present protein structural propensity data to both biology and machine learning communitites.
What is a protein structure and what is a "structure propensity" is explained below.

## Frontend (interatcive search)

For the biology-interested audience we've created the web frontend service at https://peptone.io/dspp.
You can search for the proteins you're interested in there, and we present the entries with our structural propensity predictions based on NMR chemical shift data.

## Protein sequence

Proteins are polymers - that means they are built from repeating units connected together.
Those units are called amino acids and there are 20 of them. It's like a linked list,
with amino acids connected unidirectionally, no branching, from the start to end.

What's remarkable is that the amino-acid sequence of the protein polymer determines the 3D structure of the protein and its function.
However it's unclear what the link between the sequence and the structure is - it has been focus of research for a really long time.

## Propensity

Proteins sometimes adopt very well defined, stable structure that doesn't change over time.
But that's not always true: we now know of an important category of proteins called the intrinsic disorder proteins, which do not have a well-defined structure at all. These proteins often play crucial roles in living organisms and are generally poorly understood.

So instead of thinking of protein sequence determining a structure, we prefer to think of sequence determining structural propensity. A sequence of amino acids might prefer to be structured 50% of the time but unstructured the other 50% of the time.

# Usage

To install the dspp-keras integration, just do the following

```
pip install dspp-keras
```

Or, if you're installing from source

```
python setup.py
```

To load the dataset in your python models, use the `dsppkeras.datasets` module.

```
from dsppkeras.datasets import dspp
X, Y = dspp.load_data()
```

- `X` is one-hot encoded amino-acids sequence vector

- `Y` is the ncSPC disorder predictor (bound between -1, 1), for each sequence.

An annotated example of a convolutional neural network can be found in
`examples/dspp_cnn.py`

# Issues

We are always looking forward to improving `dspp` integration for Keras.
Please file bug reports, issues or suggestions using https://github.com/PeptoneInc/dspp-keras/issues

Should you have questions related to scientific and industrial implications of **dSPP**, please
contact us at _support@peptone.io_.


# Reference
`dspp-keras` is based on ongoing scientific research into protein stability and intrinsic disorder. Therefore we suggest:
1. Download and read the **original research paper** at http://biorxiv.org/content/early/2017/06/01/144840
2. Search, browse and download complete **dSPP** database at https://peptone.io/dspp
3. Please cite this work as,
```
@article {Tamiola144840,
	author = {Tamiola, Kamil and Heberling, Matthew Michael and Domanski, Jan},
	title = {Structural Propensity Database Of Proteins},
	year = {2017},
	doi = {10.1101/144840},
	publisher = {Cold Spring Harbor Labs Journals},
	URL = {http://biorxiv.org/content/early/2017/06/01/144840},
	eprint = {http://biorxiv.org/content/early/2017/06/01/144840.full.pdf},
	journal = {bioRxiv}
}
```
