# Introduction

`dspp-keras` is a Keras integration for [Database of Structural Propensities of Proteins](https://peptone.io/dspp), which provides **amino acid sequences** of  7200+ unrelated proteins with their **propensities to form secondary structures or stay disordered**.

`dspp-keras` is based on 8+ years of research into protein disorder, folding and numerical modelling.

This is why, we strongly encourage you to read the rest of this document, scroll through the **FAQ** section, and train the test model from `example/` directory. Importantly, please read the our [Database of Structural Propensities of Proteins](http://biorxiv.org/content/early/2017/06/01/144840) paper.

## Proteins

Proteins are complex biomolecules made of 20 building blocks, amino acids, which are connected sequentially into long non-branching chains; commonly known as polypeptide chains.

Unique spatial arrangement of polypeptide chains yields 3D molecular structures, which define protein function and interactions with other biomolecules.

Although the very basic forces that govern protein 3D structure formation are known and understood, the exact nature of polypeptide folding remains elusive and has been a subject to overwhelming number of studies.

## Protein dynamics

Just like every other molecule present in our natural environment, polypeptide chains undergo molecular motions at time scales, which stretch from femtoseconds to minutes. Therefore, it is safe to say proteins owe their complexity to baffling way their polypeptide chains fold, deform and move around.

**It is accepted that complete understanding of protein functions and activity requires the knowledge of structures and dynamics.**

## Protein ensembles

Under conditions of living organisms (*aka native conditions*) in aqueous environment, protein solution of any polypeptide is in fact made of copies of molecules (*aka ensemble*), which at the given moment in time have slightly different structures, as a consequence of protein dynamics and intrinsic “flexibility”.

![MOAG-4](https://lh3.googleusercontent.com/0C95wGJf2gNsTQW84SHLCuGICJhpb6ZVTYEqkO6IG1TK4H1YjR64QlXr9GxLwwTMlJGJeU5nHN3lWN4=w1531-h914-rw)

Image above demonstrates the superposition of models belonging to structural ensemble of MOAG-4 protein, which in turn controls aggregation of proteins implicated in Parkinson’s disease. You can infer from this model that MOAG-4 has a **stable** (that is defined) **alpha-helical** structure coloured in grey, and a highly disordered tail, depicted by floating polypeptide chains of individual ensemble members.


## Protein disorder

MOAG-4 is a seminal example of protein that exhibits structural disorder, a truly perplexing property of very many polypeptides.

![Alpha-synuclein](https://lh6.googleusercontent.com/3T3ovc3Lw6hVHw-uvxIAQGyAl_6Z3m-jWSbLFIQTOUxFRMqS14HikE3kC6r_l6GTCLE052TBoIcW8Cg=w1409-h810-rw)

Alpha-synuclein, pictured above, is the most representative example of a completely disordered protein. Although the ensemble of Alpha-synuclein is completely heterogenous, this protein plays an important role in neurotransmitter mediation in human brain, and has been implicated as the key player in Parkinson’s disease development.

## Putting protein order and disorder together

Among the multitude of advanced experimental protein techniques, NMR spectroscopy offers exquisite sensitivity to structural detail and dynamics. That is why we have used NMR resonance assignment data from 7200+ proteins stored in public repositories and computed sequence-specific propensity scores.

![MOAG-4](https://lh3.googleusercontent.com/ILx35W5S6Yybg7Lk75e6yQo0aXOM6mvQpuJimmu67i64HkxUBGeNce5BQoULRBOhgX39Kzx_tO1_Ecs=w1143-h843-rw)
![Structural propensity of MOAG-4](https://lh3.googleusercontent.com/Doc_CnN5PWgfgBju2wVW1zt7G2yiqC7j_HrMpzl4xDD3k9YxEAqlz140magInT0PgG2vL9Ct1QNA1VA=w1143-h843-rw)

Consequently, the ensemble behaviour of partially disordered MOAG-4 can be characterised and compressed (with few critical assumptions [discussed in our paper](http://biorxiv.org/content/early/2017/06/01/144840)) to structural propensity vector.

Importantly, our method excels at capturing residual intrinsic disorder, as brought on example of intrinsically disordered Alpha-synuclein.


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

*Note: An annotated example of a boilerplate neural network can be found in `examples/`*.

## Training input data `X`:

A one-hot encoded amino-acids sequence vector. As an example, let's consider the amino acid sequence of [NS2B polypeptide from Zika Virus](https://peptone.io/dspp/entry/dSPP26928_0),

```python
MGSSHHHHHHSSGLVPRGSHMTGKSVDMYIERAGDITWEKDAEVTGNSPRLDVALDESGDFSLVEEDGPPMRE
```

The one-hot vector, which represents the NS2B Zika Virus seqeunce can be written as,

```python

np.array([0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], dtype=np.uint8)
```

## Training output data `Y`:

The structural propensity score tensor. Individual, residue-specific scores are bound between `-1.0` and `1.0`. Negative propensity implicates the sampling of **beta-sheet** conformations. A score of `0.0` indicates behaviour found in **disordered** proteins, whereas `1.0` is an indicator of properly folded **alpha-helix**. A score of `0.5` should be understood as a situation when 50% of ensemble members form a helix and the remaining part samples different conformations.

The propensity score vector for [NS2B polypeptide from Zika Virus](https://peptone.io/dspp/entry/dSPP26928_0) is given by,

```python
np.array([np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, -0.18, -0.30, -0.44, -0.57, -0.72, -0.41, -0.42, -0.23, -0.25, 0.06, -0.30, -0.05, -0.16, 0.17, 0.10, 0.16, 0.14, 0.21, 0.06, 0.06, 0.09, 0.07, np.nan, np.nan, np.nan, 0.02, -0.05, -0.04, -0.06, -0.03, 0.01, 0.06, 0.10, 0.14, 0.17, 0.13, 0.12, 0.05, 0.04, 0.03, -0.00, 0.09, 0.14, 0.16, np.nan, 0.16, 0.16, 0.16, 0.17], dtype=np.float32)
```

_Note: `np.nan` denotes missing experimental assignment data._

# Interactive protein search

For the biology-oriented audience and curious computational scientists we've created a web service at https://peptone.io/dspp.

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

### What’s the difference between dSPP and other protein data sets?

1. As opposed to binary (logits) secondary structure assignments available in the most protein datasets, we are in an unique position to report on protein structure and local dynamics. Please [read our paper](http://biorxiv.org/content/early/2017/06/01/144840) to learn more about the benefit of propensity inclusion.
2. Our experimental data are derived at *native conditions* rendering them absolutely unique for structure and disorder prediction methods that aim to tackle protein folding and stability in biologically relevant contexts.
3. Our dSPP user interface at https://peptone.io/dspp will give you seamless access to every single protein bundled in `dspp-keras` with all the relevant decision data, and original literature citations.

### How did you arrive at structural propensity?
It is a relatively long subject, far beyond the scope of this short document. Please [read our paper](http://biorxiv.org/content/early/2017/06/01/144840). The exact procedure is described in detail in the *Materials and Methods* together with relevant references.

### How many proteins are in dSPP?
Currently 7200+. However, the database is on an automatic **14 day** update cycle, hence we expect it to grow.

### What is the average protein length?
Currently `110` amino acids. However, the database is on an automatic update cycle, hence this number may change.

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

François Chollet [Keras](https://github.com/fchollet/keras) is greatly acknowledged for insightful feedback on database interface and straightforward suggestions concerning Keras integration.

We extend sincere thanks to Alison Lowndes, Carlo Ruiz and Dr. Adam Grzywaczewski, (NVIDIA Corporation) for facilitating collaboration and access to DGX-1 supercomputer.

Jon Wedell (BMRB) is greatly acknowledged for technical support with NMR resonance assignment retrieval from BMRB.

We thank Dr. Frans A.A. Mulder (Aarhus University, DK) and Dr. Predrag Kukic (University of Cambridge, UK) for providing structural ensemble models of MOAG-4.

Lastly, we want to greatly acknowledge Mark Berger (NVIDIA Corporation) for overwhelming support throughout the execution of this project.  
