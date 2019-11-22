# SIGMOD Reproducibility for "Uncertainty Annotated Databases - A Lightweight and General Approach for Approximating Certain Answers"


## A) Source code info

The **GProM** system is written in `C`. For the experiments we did use  [PostgreSQL](https://www.postgresql.org/) as a backend for storage. TODO
GProM is available at [https://github.com/IITDBGroup/gprom](https://github.com/IITDBGroup/gprom). For the experiments, please use the `TODO` branch. GProM acts as a client for a relational database. UA-DB creation and querying is available through an extension of SQL.

- Repository: https://github.com/IITDBGroup/gprom
- Programming Language: C, Python
- **Additional Programming Language info:** we are requiring Python3.6.9
- **Compiler Info:** TODO
- **Required libraries/packages:**
  - gnuplot (5.2)
  - pg8000
  - ... GPRoM dependencies
  - python (3.6.9)


## B)  Datasets info

We used several open real world datasets in the experiments. See below for links. We cleaned these datasets by replacing null values with constants using missing value imputation as implemented in Mimir. In the output every row with at least one replaced value was marked as uncertain. The UA-DBs generated in this ways were used in the experiments. In addition we use two synthetic datasets. One if PDBench (TODO link), a probabilistic version of the TPC-H datasets and ...
- **Real world datasets:**

| Dataset              | Rows | Cols | $U_{Attr}$ | $U_{Row}$ | URL                                                                                                        |
|----------------------|------|------|------------|-----------|------------------------------------------------------------------------------------------------------------|
| Building Violations  | 1.3M | 35   | 0.82%      | 12.8%     | https://data.cityofchicago.org/Buildings/Building-Violations/22u3-xenr                                     |
| Shootings in Buffalo | 2.9K | 21   | 0.24%      | 2.1%      | http://projects.buffalonews.com/charts/shootings/index.html                                                |
| Business Licenses    | 63K  | 25   | 1.39%      | 14.0%     | https://data.cityofchicago.org/Community-Economic-Development/Business-Licenses-Current-Active/uupf-x98q   |
| Chicago Crime        | 6.6M | 17   | 0.21%      | 0.9%      | https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-present/ijzp-q8t2                              |
| Contracts            | 94K  | 13   | 1.50%      | 19.2%     | https://data.cityofchicago.org/Administration-Finance/Contracts/rsxa-ify5                                  |
| Food Inspections     | 169K | 16   | 0.34%      | 4.6%      | https://data.cityofchicago.org/Health-Human-Services/Food-Inspections/4ijn-s7e5                            |
| Graffiti Removal     | 985K | 15   | 0.09%      | 0.8%      | https://data.cityofchicago.org/Service-Requests/311-Service-Requests-Graffiti-Removal/hec5-y4x5            |
| Building Permits     | 198K | 19   | 0.42%      | 5.3%      | https://https://www.kaggle.com/aparnashastry/building-permit-applications-data/data                        |
| Public Library Survy | 9.2K | 99   | 1.19%      | 14.2%     | https://www.imls.gov/research-evaluation/data-collection/public-libraries-survey/explore-pls-data/pls-data |

- **Data generators:**
  - `PDBench` is a probabilistic version of the TPC-H data generator, we used a fork (fixing some compilation bugs) hosted here: https://github.com/IITDBGroup/pdbench
  - To generate augment real world dataset with access control annotation, we use a python script (TODO provided as part of this repository)

## C) Hardware Info

All runtime experiments were executed on a server with the following specs:

| Element          | Description                                                                   |
|------------------|-------------------------------------------------------------------------------|
| CPU              | 2 x AMD Opteron(tm) Processor 4238, 3.3Ghz                                    |
| Caches (per CPU) | L1 (288KiB), L2 (6 MiB), L3 (6MiB)                                            |
| Memory           | 128GB (DDR3 1333MHz)                                                          |
| RAID Controller  | LSI Logic / Symbios Logic MegaRAID SAS 2108 [Liberator] (rev 05), 512MB cache |
| RAID Config      | 4 x 1TB, configured as RAID 5                                                 |
| Disks            | 4 x 1TB 7.2K RPM Near-Line SAS 6Gbps (DELL CONSTELLATION ES.3)                |


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

### Install PDBench

- TODO


### Install Postgres + load database ###

- TODO

### Run Experiments

To run all default experiments:
~~~shell
 python3 gen.py
~~~
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
