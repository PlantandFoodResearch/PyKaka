# Python API for Kaka

## Tools used

- Python 2/3
- Mongo connectors
- KAKAs restful API
- Jupyter notebooks in form of a Pyrat

## Background 

PyKaka is a Python API for downloading data from [Kaka](https://github.com/hdzierz/Kaka). The Python API works from any python 2.7 and 3.5+ python installation. Kaka can be run using docker and comes with a Pyrat pre-installed. If you e.g. load Kaka on server just-a-test.powerplant.pfr.co.nz then your Pyrat jupyter notebookd will run on just-a-test.powerplant.pfr.co.nz:8889. 

## Installation

When using A Kaka docker setup you will have a pyrat running on port 8889. You will find that the Kaka Python API has been pre-installed. Thus, the following import should just work:

```
from PyKaka.api import *
```

If it does not you need to install it via:

```
pip install git+https://github.com/hdzierz/PyKaka.git
```

## Queries
 
The syntax for the API is as follows:

```
Kaka.qry(realm='some_realm', qry='some_query', mode='a-mode') 
```

Whereby:

"realm" can currrently be:

- genotype
- design
- experiment
- term

"qry":

This is a pql query. For more info see: [pql](https://github.com/alonho/pql)

"mode":

- pql (default)
- mongo (can perform better for larger queries)

Return value:

The return value is a [pandas](http://pandas.pydata.org/) data frame.

Query for an ID:

IDs are unfirntunately a but special as we have a MongoDB in the background. I do promise to simplify this. However, teh query for an ID goes as follows:

```
dat = Kaka.qry('genotype', "_id=id(a_key)")
print(dat)

```

Or linking to a reference:

```
dat = Kaka.qry('genotype', "experiment_obj=id(a_key)")
print(dat)

```

Important is that you wrap the 'id' function around the Mongo ID. 


**Example:**

The databse is loaded with a gene expression data set. To obtain these data from Kaka you run:

```
dat = Kaka.qry('genotype', "experiment=='Gene Expression' and gene=='AT1G02930.2'")
print(dat)
```


<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>PFD1001L3R1</th>
      <th>PFD1001L3R2</th>
      <th>PFD1001L4R1</th>
      <th>PFD1001L4R2</th>
      <th>PFD1002L3R1</th>
      <th>PFD1002L3R2</th>
      <th>PFD1002L4R1</th>
      <th>PFD1002L4R2</th>
      <th>PFD2501L3R1</th>
      <th>PFD2501L3R2</th>
      <th>...</th>
      <th>experiment</th>
      <th>gene</th>
      <th>gene_name</th>
      <th>group</th>
      <th>lastupdateddate</th>
      <th>length</th>
      <th>name</th>
      <th>obs</th>
      <th>statuscode</th>
      <th>study</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>301</td>
      <td>301</td>
      <td>259</td>
      <td>270</td>
      <td>281</td>
      <td>286</td>
      <td>274</td>
      <td>266</td>
      <td>750</td>
      <td>711</td>
      <td>...</td>
      <td>gene_expression</td>
      <td>AT1G02930.2</td>
      <td>glutathione S-transferase 6</td>
      <td>unknown</td>
      <td>2016-03-04 09:45:42.372</td>
      <td>866</td>
      <td>AT1G02930.2</td>
      <td>{}</td>
      <td>1</td>
      <td>56d8a2ca32d3300001f6f338</td>
    </tr>
  </tbody>
</table>
<p>1 rows × 48 columns</p>
</div>

Gene expression data (any data really) can be supplemented with exprimental design information similar to teh old micro array targets file [targets](http://svitsrv25.epfl.ch/R-doc/library/limma/html/readTargets.html):

```
dat = Kaka.qry('design', "experiment=='Gene Expression'")
print(dat)
```

```
     phenotype  condition         typ
0  PFD1001L3R1    treated  paired-end
1  PFD1001L3R2    treated  paired-end
2  PFD1001L4R1    treated  paired-end
3  PFD1001L4R2    treated  paired-end
4  PFD1002L3R1  untreated  paired-end
5  PFD1002L3R2  untreated  paired-end
6  PFD1002L4R1  untreated  paired-end
7  PFD1002L4R2  untreated  paired-end
```



## Getting Data In

PyKaka has the ability to process data into the database. All data will be associated with an Experiment as well as a DataSource. Each Experiment and DataSource has a unique name. These names are impartant as
 all operations (delete data, reload data, load data) will be associated with them. There cannot be two Experiments or DataSources with the same name. The Experiment also requires
some basic meta info (please see config file below).

The method you can use for sending data is called "send" and is part of the Kaka api:

```
Kaka.send(data,config)
```

Whereby:

- data is your data set which can be either a pandas DataFrame or an array of dicts. **The data needs a unique ID column!** 
- config is a configuration dict

**The configuration dict:**

The configuration dict needs the following entries:

- Experiment 
 - Code: A unique name of the experiment the data are associated with. Please use characters, numbers and underscores only.
 - Date: The Date of your experiment
 - Description: A brief description of your experiment
 - Password: Allocate a password. This will protect your experiment from others overriding your data.
 - PI: Who is the PI of the experiment
 - Realm: The realm your experiment belongs to (e.g. Genotype or Seafood). You cannot create a new one. Please contact admin as above
- DataSource
 - Format: Can only be **python_dict** at the moment
 - ID Column: Your data requires a unique ID column
 - Name: This can be either a path to a file or a unique name of your data set
 - Group: Data might be grouped in an experiment like treatments [optional]
 - Creator: Who has craeted the data?
 - Contact: A contact email address 
 - Mode: Can be "Clean", "Override", "Append"

Just a wee explanation about the **Mode**:

**Override:** This will delete all data in the experiment for your DataSource before your data is loaded. 
**Clean:** This will delete all data in a DataSource associated with your experiment
**Append:** Append will not delete anything but append all data you specify to the DataSource in an Experiment 
**Destroy:** All above modes leave  trace of the experiment and DataSources. Destroy will also clean those.


** Example of a config dict for loading a hapmap into Kaka:**

```
config = {
    "DataSource":{
        "Format": "python_dict",
        "ID Column": "rs#" , 
        "Name": '/tmp/',
        "Group": "None",
        "Creator": "Helge",
        "Contact": "helge.dzierzon@plantandfood.co.nz",
    },
    "Experiment":{
        "Code": "HapMap_Test",
        "Date": "2016-01-07",
        "Description": "REST test",
        "Realm": "Genotype",
        "Mode": "Override",
        "Password": "inkl67z",
        "PI": "Willi Wimmer",
        "Species": "Cymbidium",
    }
}
```

## Configuring teh host and port

If you don't acccess the pyrat docker instance you  need to configure the host and port. PyKaka uses a cfg structure:

```
cfg["web_host"] = 'biopvm201.pfr.co.nz'
cfg["web_port"] = "8001"
Kaka.qry(..., cfg=cfg)
```



