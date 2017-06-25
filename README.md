
# Introduction

`dspp-keras` is a Keras integration for [Database of Structural Propensities of Proteins](https://peptone.io/dspp), which provides **amino acid sequences** of  7200+ unrelated proteins with their **propensities to form secondary structures or stay disordered**.

We strongly encourage you to read the rest of this document, scroll through the **FAQ** section, and train the test model from `example/` directory. Importantly, please read our [Database of Structural Propensities of Proteins](http://biorxiv.org/content/early/2017/06/01/144840) paper.

## Proteins

Proteins are complex biomolecules made of 20 building blocks, amino acids, which are connected sequentially into long non-branching chains; commonly known as polypeptide chains.

Unique spatial arrangement of polypeptide chains yields 3D molecular structures, which define protein function and interactions with other biomolecules.

Although the very basic forces that govern protein 3D structure formation are known and understood, the exact nature of polypeptide folding remains elusive and has been studied extensively.

## Protein dynamics

Just like every other molecule present in our natural environment, polypeptide chains undergo molecular motions at time scales ranging from nanoseconds to minutes.

**It is accepted that complete understanding of protein        functions and activity requires knowledge of structures and dynamics.**

## Protein ensembles

Under conditions of living organisms (*aka native conditions*) in an aqueous environment, the state of a polypeptide can be thought of as an ensemble of structures, which at any given moment in time have slightly different conformations, as a consequence of protein dynamics and intrinsic flexibility.

![MOAG-4](https://data.peptone.io/dspp-keras/MOAG-4-ensemble-1b.png)


The image above demonstrates the superposition of models belonging to a structural ensemble of MOAG-4 protein, [which in turn controls aggregation of proteins implicated in Parkinson’s disease](http://www.jbc.org/content/early/2017/03/23/jbc.M116.764886). You can infer from this model that MOAG-4 has a **stable** (well-defined) **alpha-helical** structure colored in grey, and a highly disordered tail, depicted by floating polypeptide chains of individual ensemble members.

***

_Note: MOAG-4 ensemble model has been kindly provided by Frans A.A. Mulder (Aarhus University, DK) and Dr. Predrag Kukic (University of Cambridge, UK). Please read ["MOAG-4 Promotes the Aggregation of α-Synuclein by Competing with Self-Protective Electrostatic Interactions"](http://www.jbc.org/content/early/2017/03/23/jbc.M116.764886) to learn more about this protein and its medical relevance._.

## Protein disorder

[MOAG-4 (**dSPP27058_0** in our database)](https://peptone.io/dspp/entry/dSPP27058_0) is a medically relevant example of a protein that exhibits a high degree of intrinsic structural disorder.

![Alpha-synuclein](https://data.peptone.io/dspp-keras/asyn.png)

Alpha-synuclein, pictured above, is a seminal example of a completely disordered protein. Although the ensemble of Alpha-synuclein is heterogenous, [this protein plays an important role in neurotransmitter mediation in human brain, and has been implicated as the key player in Parkinson’s disease development.](http://science.sciencemag.org/content/338/6109/949)

***
_Note: The Alpha-synuclein ensemble has been adopted from ["Structural Ensembles of Membrane-bound α-Synuclein Reveal the Molecular Determinants of Synaptic Vesicle Affinity"](https://www.nature.com/articles/srep27125)._

## Putting protein order and disorder together

Among the multitude of advanced experimental protein techniques, NMR spectroscopy offers exquisite sensitivity to structural detail and dynamics at a single residue level. We have used NMR resonance assignment data from 7200+ proteins stored in public repositories and computed sequence-specific propensity scores.

![MOAG-4](https://data.peptone.io/dspp-keras/MOAG-4-ensemble.png)
![Structural propensity of MOAG-4](https://data.peptone.io/dspp-keras/MOAG-4-propensity.png)

The ensemble behavior of partially disordered MOAG-4 can be characterized and compressed (with few critical assumptions [discussed in our paper](http://biorxiv.org/content/early/2017/06/01/144840)) to a structural propensity vector.

Importantly, our method excels at capturing residual intrinsic disorder, as seen in the example of intrinsically disordered Alpha-synuclein.

![Alpha-synuclein](https://data.peptone.io/dspp-keras/asyn.png)
![Alpha-synuclein propesnity](https://data.peptone.io/dspp-keras/asyn-propensity.png)

# Installation

To install the dspp-keras integration, just do the following

```python
pip install dspp-keras
```

Alternatively, clone the source and launch,

```python
python setup.py
```

# How to use `dspp-keras` to train models?

To load the dataset in your Python models, use the `dsppkeras.datasets` module.

```python
from dsppkeras.datasets import dspp
X, Y = dspp.load_data()
```
***

*Note: An annotated example of a boilerplate neural network can be found in `examples/`*.

## Training input data `X`:

A one-hot encoded amino acid sequence vector.

As an example, let's consider the amino acid sequence of [NS2B polypeptide from Zika Virus](https://peptone.io/dspp/entry/dSPP26928_0),

```python
MGSSHHHHHHSSGLVPRGSHMTGKSVDMYIERAGDITWEKDAEVTGNSPRLDVALDESGDFSLVEEDGPPMRE
```

The one-hot vector, which represents the NS2B Zika Virus seqeunce can be written as,

```python

np.array([0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], dtype=np.uint8)
```

## Training output data `Y`:

*The structural propensity score tensor.*

Individual, residue-specific scores are bound between `1.0` and `3.0`. A propensity of `1.0` implicates the sampling of **beta-sheet** conformations. A score of `2.0` indicates behaviour found in **disordered** proteins, whereas `3.0` is an indicator of properly folded **alpha-helix**. A score of `2.5` should be understood as a situation when 50% of ensemble members form a helix and the remaining part samples different conformations.

The propensity score vector for [NS2B polypeptide from Zika Virus](https://peptone.io/dspp/entry/dSPP26928_0) is given by,

```python
np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.82, 1.70, 1.56, 1.43, 1.28, 1.59, 1.58, 1.77, 1.75, 2.06, 1.70, 1.95, 1.84, 2.17, 2.10, 2.16, 2.14, 2.21, 2.06, 2.06, 2.09, 2.07, 0.0, 0.0, 0.0, 2.02, 1.95, 1.96, 1.94, 1.97, 2.01, 2.06, 2.10, 2.14, 2.17, 2.13, 2.12, 2.05, 2.04, 2.03, 0.00, 2.09, 2.14, 2.16, 0.0, 2.16, 2.16, 2.16, 2.17], dtype=np.float32)
```
***
_Note: `0.0` denotes missing experimental assignment data._

# Interactive protein search

For the biology-oriented audience and curious computational scientists, we've created a web service at https://peptone.io/dspp.

Use it to find proteins, explore their propensities and preview all the data in a machine learning-ready form.

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

### What’s the difference between dSPP and other protein data sets?

1. As opposed to binary (logits) secondary structure assignments available in most protein datasets, we are in a unique position to report on protein structure and local dynamics at the residue level. Please [read our paper](http://biorxiv.org/content/early/2017/06/01/144840) to learn more about the benefit of propensity inclusion.
2. Our experimental data are derived from *native conditions*, rendering them absolutely unique for structure and disorder prediction methods that aim to tackle protein folding and stability in biologically relevant contexts.
3. Our dSPP user interface at https://peptone.io/dspp will give you seamless access to every single protein bundled in `dspp-keras` with all the relevant decision data and original literature citations.

### How did you arrive at structural propensity?
It is a relatively long subject, far beyond the scope of this short document. Please [read our paper](http://biorxiv.org/content/early/2017/06/01/144840). The exact procedure is described in detail in the *Materials and Methods* together with relevant references.

### How many proteins are in dSPP?
Currently 7200+. However, the database is on an automatic **14 day** update cycle, hence we expect it to grow.

### What is the average protein length?
Currently `120` amino acids. However, the database is on an automatic update cycle, hence this number may change.

### What about experimental conditions relevant to dSPP data?
The experimental data in dSPP have been collected in solution and solid state NMR experiments. The average experimental temperature is `295K`, pH of `6.9` and ionic strength of `~100mM`. Please [read our paper](http://biorxiv.org/content/early/2017/06/01/144840) to learn more.

### I am data scientist. I would like to know more about the raw data?
We have you covered! Simply navigate to https://peptone.io/dspp and open up *Database statistics* panel. All the database statistics are recomputed for dSPP every 14 days.

### Can I contribute to dSPP data-set?
Yes. If you happen to have a newly assigned protein, please follow the submission procedure to [BMRB](http://www.bmrb.wisc.edu/). As only your data becomes available in BMRB and passes our quality checks we will include it in our repository.

### Are you planning to bundle more features with dSPP?
Yes. We are actively developing on an expansion of dSPP, which will contain additional experimental data to model protein stability and local dynamics.

# Acknowledgements

We want to acknowledge Dr. Wenwei Zheng (NIDDK, US), Dr. Ruud Scheek (University of Groningen, NL) and Dr. Xavier Periole (Aarhus University, DK) for insightful comments and editorial suggestions concerning our [dSPP paper](http://biorxiv.org/content/early/2017/06/01/144840).

[François Chollet](https://github.com/fchollet) of [Keras / Google](https://github.com/fchollet/keras) is greatly acknowledged for insightful feedback on database interface and straightforward suggestions concerning Keras integration.

We extend sincere thanks to Alison Lowndes, Carlo Ruiz and Dr. Adam Grzywaczewski, (NVIDIA Corporation) for facilitating collaboration and access to DGX-1 supercomputer.

Jon Wedell (BMRB) is greatly acknowledged for technical support with NMR resonance assignment retrieval from BMRB.

We thank Dr. Frans A.A. Mulder (Aarhus University, DK) and Dr. Predrag Kukic (University of Cambridge, UK) for providing structural ensemble models of MOAG-4.

Lastly, we want to greatly acknowledge Mark Berger (NVIDIA Corporation) for overwhelming support throughout the execution of this project.  
