# SIGMOD Reproducibility for "Uncertainty Annotated Databases - A Lightweight and General Approach for Approximating Certain Answers"


## A) Source code info

The **GProM** system is written in `C`. For the experiments we did use  [PostgreSQL](https://www.postgresql.org/) as a backend for storage. TODO
GProM is available at [https://github.com/IITDBGroup/gprom](https://github.com/IITDBGroup/gprom). For the experiments, please use the `TODO` branch. GProM acts as a client for a relational database. UA-DB creation and querying is available through an extension of SQL.

- Repository: https://github.com/IITDBGroup/gprom
- Programming Language: C, Python
- **Additional Programming Language info:** we are requiring PythonX. TODO
- **Compiler Info:** TODO
- **Required libraries/packages:**
  - gnuplot (TODO versions?)
  - ps2pdf
  - ... GPRoM dependencies
  - python (TODO version)


## B)  Datasets info

We used several real world datasets in the experiments. In addition we use two synthetic datasets. One if PDBench (TODO link), a probabilistic version of the TPC-H datasets and ...
- **Repository:** [url]
- **Data generators:**

## C) Hardware Info
[Here you should include any details and comments about the used hardware in order to be able to accommodate the reproducibility effort. Any information about non-standard hardware should also be included. You should also include at least the following info:]

TODO
- C1) Processor (architecture, type, and number of processors/sockets)
- C2) Caches (number of levels, and size of each level)
- C3) Memory (size and speed)
- C4) Secondary Storage (type: SSD/HDD/other, size, performance: random read/sequnetial read/random write/sequnetial write)


## D) Installation and Setup

### Install GProM

Please follow these instructions to install the system and datasets for reproducibility.

#### Prerequisites ####

GProM requires TODO. For example, on Ubuntu you can install the prerequisites with:

~~~shell
sudo apt-get install
~~~

#### Clone git repository

Please clone the git repository ...

~~~shell
git clone git@github.com:IITDBGroup/gprom ...
~~~

#### Build and Install GProM

As mentioned before, Cape is written in Python. We recommend creating a python3 [virtual environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/). There are several ways to do that. Here we illustrate one. First enter the directory in which you cloned the capexplain git repository.


- TODO

### Install Postgres + load database ###

- TODO

### Run Experiments

To run all default experiments:
> python3 gen.py

The script will create a folder /result containing all test results in form of .csv(tables) and .pdf(plots).

### Suggestions and Instructions for Alternative Experiments


- TODO


# Appendix (previous instructions)

Requirements for plotting:
	gnuplot
	ps2pdf

Configure connection detials for postgres in config/database.ini

PDbench tests:
	For this automated test, each pdbench test with corresponding factors will generate data in a distinct folder. For each time and result size test, the corresponding folder will be loaded into postgres and run queries over it. For next test previous tables will be removed.
	Test can be extended onto different scale factors by modifying the input list.
	varying uncertainty:
		default sacle factor: 1 (1=1GB)
		default uncertainty factor list: [0.02, 0.05, 0.1, 0.3]
	varying data scale:
		default uncertainty factor: 0.02
		default scale factor list: [0.1, 1, 10]
	Extra queries can be used only for conventional query processing, UADB and MCDB since we can not get automated rewriting systems from Libkins and Maybms approach.
