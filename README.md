# Introduction

`dspp-keras` is a Keras integration for Database of Structural Propensities of Proteins, which provides **amino acid sequences** of  7200+ unrelated proteins with their **propensities to form secondary structures or stay disordered**.

To fully understand and explore the potential of `dspp-keras` we strongly encourage you to read the rest of this document, scroll through the **FAQ** section, and train the test model from `example/` directory.

## Proteins

Proteins are complex biomolecules made of 20 building blocks, amino acids, which are connected sequentially into long non-branching chains; commonly known as polypeptide chains.

Unique spatial arrangement of polypeptide chains yields 3D molecular structures, which define protein function and interactions with other biomolecules.

Although the very basic forces that govern protein 3D structure formation are known and understood, the exact nature of polypeptide folding remains elusive and has been a subject to overwhelming number of studies.

## Protein dynamics

Just like every other molecule present in our natural environment, polypeptide chains undergo molecular motions at time scales, which stretch from femtoseconds to minutes. Therefore, it is safe to say proteins owe their complexity to baffling way their polypeptide chains fold, deform and move around.

**It is accepted that unravelling of protein functions and activity mechanisms requires the knowledge of structures and dynamics.**

## Protein ensembles

Under conditions of living organisms (*aka native conditions*) in aqueous environment, protein solution of any polypeptide is in fact made of copies of molecules (*aka ensemble), which at given moment in time have slightly different structures, as a consequence of protein dynamics.

[MOAG]

Image above demonstrates the superposition of models belonging to structural ensemble of MOAG-4 protein, which in turn controls aggregation of proteins implicated in Parkinson’s disease. You can infer from this model that MOAG-4 has a **stable** (that is defined) **alpha-helical** structure coloured in blue, and a highly disordered tail, depicted by floating polypeptide chains of individual ensemble members.


## Protein disorder

MOAG-4 is a seminal example of protein that exhibits structural disorder, a truly perplexing property of very many polypeptides. Alpha-synuclein, pictured below, is the most representative example of a completely disordered protein. Although the ensemble of Alpha-synuclein is completely heterogenous, this protein plays an important role in neurotransmitter mediation in human brain, and has been implicated as the key player in Parkinson’s disease development.

[ASYN]

## Putting protein order and disorder together

We have used NMR resonance assignment data from 7200+ proteins collected in public repositories to compute sequence-specific propensity scores. Please [read our paper](http://biorxiv.org/content/early/2017/06/01/144840) to learn more about the exact calculation procedure and other technical details.


# Installation

To install the dspp-keras integration, just do the following

```
pip install dspp-keras
```

Alternatively, clone the source and launch,

```
python setup.py
```

# How to use `dspp-keras` to train models?

To load the dataset in your python models, use the `dsppkeras.datasets` module.

```
from dsppkeras.datasets import dspp
X, Y = dspp.load_data()
```

*Note: An annotated example of a boilerplate neural network can be found in `examples/`*.

## Input data (X):

A one-hot encoded amino-acids sequence vector.

## Output data (Y):

The structural propensity score tensor. Individual, residue-specific scores are bound between `-1.0` and `1.0`. Negative propensity implicates the sampling of **beta-sheet** conformations. A score of `0.0` indicates behaviour found in **disordered** proteins, whereas `1.0` is an indicator of properly folded protein. A score of `0.5` should be understood as a situation when 50% of ensemble members form a helix and the remaining part samples different conformations.

# Interactive protein search

For the biology-oriented audience we've created a web service at https://peptone.io/dspp.

Use it to find proteins, explore their propensities and preview all the data in machine-learning ready form.

# Issues

We are always looking forward to improving `dspp` integration for Keras and Tensorflow.

Please file bug reports, issues or suggestions using https://github.com/PeptoneInc/dspp-keras/issues

Should you have questions related to scientific and industrial implications of **dSPP**, please contact us at _support@peptone.io_.

# References
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

# Frequently Asked Questions

### What does dSPP stand for?

dSPP - Database of Structural Propensities of Proteins
