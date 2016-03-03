# Python API for Kaka

## Tools

- R/knitr
- Python 2/3
- Mongo connectors
- KAkAs restful API
- Jupyter notebooks in form of a Pyrat

## Background 


The Python API works from any python 2.7 and 3.5+ python installation. Kaka itself comes with a Pyrat pre-installed. If you e.g. load Kaka on server just-a-test.powerplant.pfr.co.nz then your Pyrat jupyter notebookd will run on just-a-test.powerplant.pfr.co.nz:8889. 

You can use the API though in a "plain" python script. 

When using A Kaka docker setup you will have a pyrat running on port 8889. You will find that the Kaka Python API has been pre-installed. Thus, the following import just works:

```
from Kaka.api import *
```

If it does not you need to install it via:

```
pip install git+https://github.com/hdzierz/PyKaka.git
```

### Queries
 
The syntax for the API is as follows:

```
Kaka.qry(realm='some_realm', qry='some_query', mode='a-mode') 
```

Whereby:

"realm" can currrently be:

- genotype
- seafood

"qry":

This is a pql query. For more info see: [pql](https://github.com/alonho/pql)

"mode":

- pql (default)
- mongo (can perform better for larger queries)

Return value:

The return valeu is a pandas data frame.

**Example:**

To obtain data from Kaka you run (:

```
dat = Kaka.qry('genotype', "experiment=='gene_expression' and gene='AT1G02930.2'")
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



