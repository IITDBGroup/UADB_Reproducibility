# SIGMOD Reproducibility for "Uncertainty Annotated Databases - A Lightweight and General Approach for Approximating Certain Answers"


## A) Source code info

The **GProM** system is written in `C`. For the experiments we did use  [PostgreSQL](https://www.postgresql.org/) as a backend for storage. TODO
GProM is available at [https://github.com/IITDBGroup/gprom](https://github.com/IITDBGroup/gprom). For the experiments, please use the `TODO` branch. GProM acts as a client for a relational database. UA-DB creation and querying is available through an extension of SQL.

- Repository: https://github.com/IITDBGroup/gprom
- Programming Language: C, Python
- **Additional Programming Language info:** we are requiring Python3.6.9
- **Compiler Info:** gcc-11.0.0
- **Required libraries/packages:**
  - gnuplot (5.2)
  - pg8000
  - GPRoM dependencies
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
  - For real world dataset with access control annotation, we generate the data in the python testing script.

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

### Docker installation of the whole experiment envirnment

A docker hub is prepared with all requirements installed,

You can pull the docker image with:
~~~shell
docker pull iitdbgroup/uadbreproduce
~~~
The image entry point is set to /bin/bash, so to load the docker image in command line:
~~~shell
docker run -ti iitdbgroup/uadbreproduce
~~~
The main test script is under the default entry folder.
All test results is saved to /results folder. To get the results in local system, mount a local system folder to the docker container result folder when load the image:
~~~shell
docker run -ti -v /your/local/directory:/reproducibility/results iitdbgroup/uadbreproduce 
~~~

### strp by step installations (not required if use docker)

#### Install GProM

Please follow these instructions to install the system and datasets for reproducibility.

##### Prerequisites #####

GProM requires TODO. For example, on Ubuntu you can install the prerequisites with:
~~~shell
sudo apt-get install
~~~

##### Clone git repository

Please clone the git repository ...

~~~shell
git clone git@github.com:IITDBGroup/gprom ...
~~~

##### Build and Install GProM

As mentioned before, Cape is written in Python. We recommend creating a python3 [virtual environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/). There are several ways to do that. Here we illustrate one. First enter the directory in which you cloned the capexplain git repository.

- TODO

#### Install PDBench

Our python script will make and generate PDbench data when needed by the experiments.
The data will be saved into a folder with name s[sval]x[xval] where sval is the scale factor and xval is the uncertainy factor.

#### Install Postgres + load database ####

By default the python testing script will connect to database 'postgres' with port 5432. Connection can be configured in the /config/config.ini file. 

# Run Experiments

We provide a unified python script file (gen.py) to run all experiments.
To run all default experiments:
~~~shell
 python3 gen.py
~~~
The schript will record which tests are done so when reruning the script it will not repeat finshed tests.
To start from beginning of the test, use command -r:
~~~shell
 python3 gen.py -r
~~~
The script also allowing executing only one experiment
for specifying a single experiment/step using -s:
~~~shell
-s command values:

0 - prepair sqlite database data.

1 - pdbench data generation on all test cases.

2 - perform pdbench test varying amount of uncertainty.

3 - perform pdbench test varying data size.

4 - perform pdbench result size test.

5 - perform incompetness projection test.

6 - perform ultility test.

7 - perform realQuery test.
~~~

For example, to run only pdbench test by varying result size and regenerate data using pdbench:
~~~shell
 python3 gen.py -r -s 4
~~~

## Get experiment results
All experiment results will be save to /result folder. 

# Suggestions and Instructions for Alternative Experiments

## PDBench experiments with different parameter settings

Different parameter settings need to modify the 's' list and 'x' list in the gen.py file where 's' is the list of all scale factors will be tested and 'x' is the list of all uncertainty factors will be tested.

## Running ad hoc queries through GProM

You can use the gprom system included in the container to run queries with UA-DB semantics over the provided datasets.

### GProM UA-DB Syntax

To run a query with uncertain semantics, the whole query should be wrapped in:

~~~sql
TUPLE UNCERTAIN (
    ...
);
~~~

Unless instructed otherwise, GProM expects inputs to be UA-DBs. However, GProM can also interpret different types of uncertain data models and translate them into UA-DBs as part of queries. To inform GProM that an input table should be interpreted as a certain type of uncertain relation, you specify the type after the table access in the `FROM` clause. Currently, we support tuples-independent probabilistic databases (TIPS) and x-relations.

#### TIPs

A TIP stores for each row it's marginal probability. The existence of tuples in the database are assumed to be mutually independent of each other. That is, the set of possible worlds represented by a TIP database are all subsets of the TIP database. To use a TIP table in GProM, the table should have an additional attribute storing the tuple probabilities and the table access in the `FROM` clause should be followed by `IS TIP (prob)` where `prob` is the name of the attribute storing tuple probabilities. For instance, consider this table `R` (attribute `p` stores probabilities):

```sql
| name  | age | p  |
|-------|-----|----|
| Peter | 34 | 0.9 |
| Alice | 19 | 0.6 |
| Bob   | 23 | 1.0 |
```

An example query over this table

~~~sql
TUPLE UNCERTAIN (
  SELECT * FROM R IS TIP(p);
);
~~~

#### X-DBs

An X-table consists of x-tuples which are sets of tuples called alternatives, each associated with a probability. X-tables are a specific type of block-independent probabilistic databases. The alternatives of an x-tuple are disjoint events while alternatives from different x-tuples are independent events. GProM expects an X-tables to have two additional attributes: one that stores probabilities for alternatives and one that stores a unique identifier for each x-tuple. For instance, consider the following table where we are uncertain about Peter's age, and Alice may or may not be in the table.

```sql
| name  | age | x-id |  p  |
|-------|-----|------|----|
| Peter | 34 | 1     | 0.4 |
| Peter | 35 | 1     | 0.3 |
| Peter | 36 | 1     | 0.3 |
| Alice | 19 | 2     | 0.6 |
| Bob   | 23 | 3     | 1.0 |
```

To use a X-table in GProM you have to specify the names of the attributes storing probabilities and x-tuple identifiers. For instance, for the table above:

~~~sql
TUPLE UNCERTAIN (
  SELECT * FROM R IS XTABLE(x-id,p);
);
~~~

### Pointers

To run queries over the provided datasets use start gprom like this:
(You need to unzip the database if it is not done by the testing script)

~~~sh
gprom -backend sqlite -db /reproducibility/dbs/incomp.db
~~~

#### Table names
buffalo

#### Example Queries

~~~sql
TUPLE UNCERTAIN (SELECT "lat" FROM buffalo IS UADB);
~~~
