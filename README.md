# iData

## Why imfidata?

IMF’s SDMX endpoints power gems like CPI, GFS, and WEO. The official
snippets are useful but not exactly beginner-friendly. This guide shows
a clean, reproducible workflow using the `imfidata` package—focusing on:

- Discovering datasets (including internal/auth-gated ones)
- Inspecting **dimensions** and **codelists**
- Building valid **keys** with autocompletion
- Downloading tidy data you can analyze immediately

> If you’re new to SDMX: think of a dataset as a table, **dimensions**
> as the “fields” you must specify (e.g., country, indicator,
> frequency), and a **key** as the compact string that selects the slice
> you want.

------------------------------------------------------------------------

## Setup

### 1) Install

``` python
# If you don't have imfidata yet run the following from a command line
# pip install git+https://github.com/BasBBakkerIMF/imfidata.git
```

### 2) Import

``` python
import imfidata as idata
```

------------------------------------------------------------------------

## Explore: what datasets are available?

### List all public IMF datasets

``` python
mydatasets = idata.metadata.show_imf_datasets()
mydatasets
```

<div>

<div>

|     | id                  | version | agencyID | name_en                                           |
|-----|---------------------|---------|----------|---------------------------------------------------|
| 0   | AFRREO              | 6.0.1   | IMF.AFR  | Sub-Saharan Africa Regional Economic Outlook (... |
| 1   | HPD                 | 1.0.0   | IMF.FAD  | Historical Public Debt (HPD)                      |
| 2   | PI                  | 2.0.0   | IMF.STA  | Production Indexes (PI)                           |
| 3   | APDREO              | 6.0.0   | IMF.APD  | Asia and Pacific Regional Economic Outlook (AP... |
| 4   | MFS_ODC             | 9.0.1   | IMF.STA  | Monetary and Financial Statistics (MFS), Other... |
| ... | ...                 | ...     | ...      | ...                                               |
| 62  | FSIC                | 13.0.1  | IMF.STA  | Financial Soundness Indicators (FSI), Core and... |
| 63  | ANEA                | 6.0.1   | IMF.STA  | National Economic Accounts (NEA), Annual Data     |
| 64  | ISORA_2018_DATA_PUB | 2.0.0   | ISORA    | ISORA 2018 Data                                   |
| 65  | FM                  | 5.0.0   | IMF.FAD  | Fiscal Monitor (FM)                               |
| 66  | GFS_COFOG           | 11.0.0  | IMF.STA  | GFS Government Expenditures by Function           |

<p>67 rows × 4 columns</p>
</div>

</div>

You’ll get a DataFrame with columns like `id`, `name`, `agencyID`, etc.

### Filter by agency (example: FAD)

``` python
res = mydatasets.query("agencyID == 'IMF.FAD'")
res
```

<div>

<div>

|     | id   | version | agencyID | name_en                                     |
|-----|------|---------|----------|---------------------------------------------|
| 1   | HPD  | 1.0.0   | IMF.FAD  | Historical Public Debt (HPD)                |
| 19  | GDD  | 2.0.0   | IMF.FAD  | Global Debt Database (GDD)                  |
| 38  | ICSD | 1.0.0   | IMF.FAD  | Investment and Capital Stock Dataset (ICSD) |
| 65  | FM   | 5.0.0   | IMF.FAD  | Fiscal Monitor (FM)                         |

</div>

</div>

### Check if a dataset is accessible (WEO_LIVE)

``` python
weolive = mydatasets.query("id == 'WEO_LIVE'")
weolive
```

<div>

<div>

|     | id  | version | agencyID | name_en |
|-----|-----|---------|----------|---------|

</div>

</div>

`WEO_LIVE` requires authentication. Let’s now include internal datasets.

### Include internal/auth-gated datasets

``` python
mydatasets = idata.metadata.show_imf_datasets(needs_auth=True)
mydatasets
```

<div>

<div>

|     | id       | version | agencyID | name_en                                           |
|-----|----------|---------|----------|---------------------------------------------------|
| 0   | CFBL     | 1.0.0   | IMF.STA  | Carbon Footprint of Bank Loans (CFBL)             |
| 1   | IIPCC    | 13.0.0  | IMF.STA  | Currency Composition of the International Inve... |
| 2   | FSICDM   | 7.0.0   | IMF.STA  | Financial Soundness Indicators (FSI), Concentr... |
| 3   | ICSD     | 1.0.0   | IMF.FAD  | Investment and Capital Stock Dataset (ICSD)       |
| 4   | WTOIMFTT | 2.0.1   | WTO      | WTO-IMF Tariff Tracker (WTOIMFTT)                 |
| ... | ...      | ...     | ...      | ...                                               |
| 80  | GDD      | 2.0.0   | IMF.FAD  | Global Debt Database (GDD)                        |
| 81  | ITG      | 4.0.0   | IMF.STA  | International Trade in Goods (ITG)                |
| 82  | GPI      | 3.0.0   | IMF.STA  | Government Policy Indicators (GPI)                |
| 83  | MFS_DC   | 7.0.1   | IMF.STA  | Monetary and Financial Statistics (MFS), Depos... |
| 84  | APDREO   | 6.0.0   | IMF.APD  | Asia and Pacific Regional Economic Outlook (AP... |

<p>85 rows × 4 columns</p>
</div>

</div>

``` python
weolive = mydatasets.query("id == 'WEO_LIVE'")
weolive
```

<div>

<div>

|     | id       | version | agencyID    | name_en                           |
|-----|----------|---------|-------------|-----------------------------------|
| 38  | WEO_LIVE | 3.0.0   | IMF.RES.WEO | World Economic Outlook (WEO) Live |

</div>

</div>

------------------------------------------------------------------------

## Dimensions: what fields do I need?

Each dataset defines its variables in a **Data Structure Definition
(DSD)**.

### Example: WEO

``` python
dimensions = idata.metadata.get_dimension_names("WEO")
dimensions
```

<div>

<div>

|     | dimension   | codelists        |
|-----|-------------|------------------|
| 0   | COUNTRY     | CL_WEO_COUNTRY   |
| 1   | INDICATOR   | CL_WEO_INDICATOR |
| 2   | FREQUENCY   | CL_FREQ          |
| 3   | TIME_PERIOD | None             |

</div>

</div>

### Example: CPI

``` python
dimensions = idata.metadata.get_dimension_names("CPI")
dimensions
```

<div>

<div>

|     | dimension              | codelists                     |
|-----|------------------------|-------------------------------|
| 0   | COUNTRY                | CL_COUNTRY                    |
| 1   | INDEX_TYPE             | CL_INDEX_TYPE                 |
| 2   | COICOP_1999            | CL_COICOP_1999                |
| 3   | TYPE_OF_TRANSFORMATION | CL_CPI_TYPE_OF_TRANSFORMATION |
| 4   | FREQUENCY              | CL_FREQ                       |
| 5   | TIME_PERIOD            | None                          |

</div>

</div>

You’ll see the dimension “names” you must populate when building a key
(e.g., country, index type, COICOP, transformation, frequency).

``` python
dimenvs=idata.metadata.get_dimension_name_env("CPI")
dimenvs.TYPE_OF_TRANSFORMATION
```

    'CL_CPI_TYPE_OF_TRANSFORMATION'

------------------------------------------------------------------------

## Developer-friendly keys with autocompletion

Typing cryptic SDMX codes by hand is… not fun. `imfidata` can generate
Python “environments” that **autocomplete** descriptive names to the
right codes.

### Build environments for CPI dimensions

``` python
transforms_df, transforms=idata.metadata.get_subcodelist("CPI", 'CL_CPI_TYPE_OF_TRANSFORMATION') 

transforms_df, transforms=idata.metadata.get_subcodelist("CPI", dimenvs.COICOP_1999) 

transforms_df
```

<div>

<div>

|     | code_id | name                                              | description                                       |
|-----|---------|---------------------------------------------------|---------------------------------------------------|
| 0   | CP01    | Food and non-alcoholic beverages                  | Food and non-alcholoic beverages consumer pric... |
| 1   | CP02    | Alcoholic beverages, tobacco and narcotics        | Alcoholic beverages, tobacco and narcotics con... |
| 2   | CP03    | Clothing and footwear                             | Clothing and footwear consumer price index is ... |
| 3   | CP04    | Housing, water, electricity, gas and other fuels  | Housing, water, electricity, gas and other fue... |
| 4   | CP05    | Furnishings, household equipment and routine h... | Furnishings, household equipment and routine h... |
| 5   | CP06    | Health                                            | Health consumer price index is produced using ... |
| 6   | CP07    | Transport                                         | Transport consumer price index is produced usi... |
| 7   | CP08    | Communication                                     | Communication consumer price index is produced... |
| 8   | CP09    | Recreation and culture                            | Recreation and culture consumer price index is... |
| 9   | CP10    | Education                                         | Education consumer price index is produced usi... |
| 10  | CP11    | Restaurants and hotels                            | Restaurants and hotels consumer price index is... |
| 11  | CP12    | Miscellaneous goods and services                  | Miscellaneous goods and services consumer pric... |
| 12  | CP13    | Individual consumption expenditure of non-prof... | Individual consumption expenditure of non-prof... |
| 13  | CP14    | Individual consumption expenditure of general ... | Individual consumption expenditure of general ... |
| 14  | \_T     | All Items                                         | All items in the context of the consumer price... |

</div>

</div>

``` python
indexes_df,indexes=idata.metadata.get_subcodelist("CPI",  dimenvs.INDEX_TYPE)
indexes_df
```

<div>

<div>

|     | code_id              | name                                              | description                                       |
|-----|----------------------|---------------------------------------------------|---------------------------------------------------|
| 0   | BSI                  | Bank stock index                                  | A financial index that tracks the performance ... |
| 1   | CCPI                 | Core consumer price index (CPI)                   | A measure of the price level of consumer goods... |
| 2   | CCPISVN              | Core consumer price index (CCPI) (SVN)            |                                                   |
| 3   | CECO                 | Commodity price index, energy, crude oil (petr... | The Commodity Price Index for energy, crude oi... |
| 4   | CEMPI                | Commodity net export price index                  | Represents the difference in the trends of exp... |
| 5   | CEPI                 | Commodity export price index                      | A measure that tracks the changes over time in... |
| 6   | CHICPIF              | Core HICP inflation forecast                      | The Core Harmonised Index of Consumer Prices (... |
| 7   | CMPI                 | Commodity import price index                      | This index measures the changes in the prices ... |
| 8   | CPCE                 | Core PCE Price Index                              | The Core Personal Consumption Expenditures (PC... |
| 9   | CPI                  | Consumer price index (CPI)                        | The Consumer Price Index (CPI) is an index of ... |
| 10  | CPIR                 | Relative consumer price index (CPI)               | The CPI of the country compared to the trade-w... |
| 11  | CPIU                 | Consumer price index (Urban)                      | The Consumer Price Index (Urban), often abbrev... |
| 12  | CPIX                 | Commodity price index                             | A commodity price index is a measurement tool ... |
| 13  | D                    | Deflator                                          | A measure used to adjust nominal values for in... |
| 14  | DMN_EMP_CR_SQSCLD    | Flexible exchange market pressure index           | Measures the pressure on a country's exchange ... |
| 15  | EPI                  | Export price index (XPI)                          | An index that measures the price changes of go... |
| 16  | FSI                  | Financial stress indicators                       | Quantitative measures that signal the level of... |
| 17  | HFIDX                | Herfindahl index                                  | A measure of market concentration and competit... |
| 18  | HICP                 | Harmonised index of consumer prices (HICP)        | The Harmonised Index of Consumer Prices (HICP)... |
| 19  | IPIX                 | Industrial production index (IPI)                 | Industrial Production Index (IPI) is a monthly... |
| 20  | L                    | Chain linked volume                               | A volume measure that adjusts for changes in p... |
| 21  | LR                   | Chain linked volume (rebased)                     | A chain linked volume measure that has been re... |
| 22  | MPI                  | Import price index                                | An index that measures the price changes of go... |
| 23  | NEER                 | Nominal effective exchange rate (NEER)            | A nominal effective exchange rate (NEER) is a ... |
| 24  | PD                   | Price deflator                                    | An economic indicator used to adjust nominal e... |
| 25  | PPI                  | Producer price index (PPI)                        | The Producer Price Index (PPI) is a key econom... |
| 26  | REER                 | Real effective exchange rate (REER)               | A real effective exchange rate (REER) is a mea... |
| 27  | RSI                  | Retail sales index                                | The Retail Sales Index (RSI) measures the mont... |
| 28  | SQRMSCINC_RET_SQSCLD | Financial price index                             | A composite index that tracks the movement of ... |
| 29  | STKRET               | Stock returns                                     | Measures the profit or loss generated on an in... |
| 30  | THEIL                | Theil index                                       | A Theil index can be interpreted as a measure ... |
| 31  | TT                   | Terms of trade (TOT)                              | The ratio of export prices to import prices, i... |
| 32  | VI                   | Volume index                                      | Index showing the average of the proportionate... |
| 33  | WPI                  | Wholesale price index (WPI)                       | The Wholesale Price Index (WPI) measures chang... |
| 34  | PDE                  | Price deflator (Eurostat)                         | An economic indicator used to adjust nominal e... |
| 35  | UVD                  | Unit value deflator                               | A price index constructed by comparing the ave... |
| 36  | REER_ASM             | REER % ASM                                        |                                                   |
| 37  | CPPI                 | Core producer price index (Core PPI)              | The Producer price index (PPI) is a key econom... |
| 38  | PMI                  | Purchasing managers index (PMI)                   | The Purchasing Managers’ Index (PMI) is a mont... |
| 39  | HIPP                 | Harmonised index of producer prices (HIPP)        | The Harmonised Index of Producer Prices (HICP)... |
| 40  | FMSCI                | Morgan Stanley MSCI stock price index             |                                                   |
| 41  | TTG                  | Terms of trade (TOT) Goods                        | The ratio of export of goods prices to import ... |
| 42  | PD_EUR               | Price deflator (EUR)                              | An economic indicator used to adjust nominal e... |
| 43  | PD_USD               | Price deflator (USD)                              | An economic indicator used to adjust nominal e... |
| 44  | PD_XDR               | Price deflator (SDR)                              | An economic indicator used to adjust nominal e... |
| 45  | PIX                  | Production index                                  | Production Index is a indicator that measures ... |
| 46  | CCPIXFEN             | Core inflation excluding food and energy          | Core inflation excluding food and energy.         |
| 47  | PCPIHACO             | Core inflation including housing                  | Core inflation including housing.                 |
| 48  | CPISRP               | Consumer price index (CPI) common reference pe... | The Consumer Price Index (CPI) is an index of ... |

</div>

</div>

Type `indexes.` in your editor and let autocomplete reveal options like
`Consumer_price_index_CPI`. Selecting it yields the correct code at
runtime.

``` python
coicops_df,coicops = idata.metadata.get_subcodelist("CPI", dimenvs.COICOP_1999)

coicops_df
```

<div>

<div>

|     | code_id | name                                              | description                                       |
|-----|---------|---------------------------------------------------|---------------------------------------------------|
| 0   | CP01    | Food and non-alcoholic beverages                  | Food and non-alcholoic beverages consumer pric... |
| 1   | CP02    | Alcoholic beverages, tobacco and narcotics        | Alcoholic beverages, tobacco and narcotics con... |
| 2   | CP03    | Clothing and footwear                             | Clothing and footwear consumer price index is ... |
| 3   | CP04    | Housing, water, electricity, gas and other fuels  | Housing, water, electricity, gas and other fue... |
| 4   | CP05    | Furnishings, household equipment and routine h... | Furnishings, household equipment and routine h... |
| 5   | CP06    | Health                                            | Health consumer price index is produced using ... |
| 6   | CP07    | Transport                                         | Transport consumer price index is produced usi... |
| 7   | CP08    | Communication                                     | Communication consumer price index is produced... |
| 8   | CP09    | Recreation and culture                            | Recreation and culture consumer price index is... |
| 9   | CP10    | Education                                         | Education consumer price index is produced usi... |
| 10  | CP11    | Restaurants and hotels                            | Restaurants and hotels consumer price index is... |
| 11  | CP12    | Miscellaneous goods and services                  | Miscellaneous goods and services consumer pric... |
| 12  | CP13    | Individual consumption expenditure of non-prof... | Individual consumption expenditure of non-prof... |
| 13  | CP14    | Individual consumption expenditure of general ... | Individual consumption expenditure of general ... |
| 14  | \_T     | All Items                                         | All items in the context of the consumer price... |

</div>

</div>

### Transformation codes

``` python
transforms_df,transforms = idata.metadata.get_subcodelist("CPI", dimenvs.TYPE_OF_TRANSFORMATION)
transforms_df
```

<div>

<div>

|     | code_id           | name                                              | description                                       |
|-----|-------------------|---------------------------------------------------|---------------------------------------------------|
| 0   | IX                | Index                                             | A statistical measure that expresses the relat... |
| 1   | POP_PCH_PA_PT     | Period average, Period-over-period percent change | Average percentage change of the data series o... |
| 2   | YOY_PCH_PA_PT     | Period average, Year-over-year (YOY) percent c... | The percentage change over two consecutive yea... |
| 3   | WGT               | Weight                                            | Weight refers to a numerical value assigned to... |
| 4   | WGT_PT            | Weight, Percent                                   | Weight refers to a numerical value assigned to... |
| 5   | SRP_IX            | Standard reference period (2010=100), Index       | Standard Reference Period (SRP) is a consisten... |
| 6   | SRP_POP_PCH_PA_PT | Standard reference period (2010=100), Period a... | Standard Reference Period (SRP) is a consisten... |
| 7   | SRP_YOY_PCH_PA_PT | Standard reference period (2010=100), Period a... | Standard Reference Period (SRP) is a consisten... |

</div>

</div>

------------------------------------------------------------------------

## Build a CPI key (countries × index × COICOP × transform × freq)

**Rule of thumb:** Don’t pass raw strings when an environment is
available—use the autocompleted objects so you get valid codes. Also put
entries in **lists**, not raw strings.

``` python
mycountries  = ["USA", "NLD"]  # ISO3
myindexes    = [indexes.Consumer_price_index_CPI]
mycoicops    = [coicops.All_Items]
mytransforms = [transforms.Index]
myfreq       = ["M"]  # monthly

key    = [mycountries, myindexes, mycoicops, mytransforms, myfreq]
keystr = idata.utils.make_key_str(key)
keystr
```

    'USA+NLD.CPI._T.IX.M'

`keystr` is your SDMX key string (e.g., `USA+NLD.CPI.ALL...M`)—compact
and valid.

------------------------------------------------------------------------

## Download CPI data

``` python
cpi = idata.retrieval.imfdata_by_key(dataset="CPI", key=keystr)
cpi
```

<div>

<div>

|      | INDEX_TYPE | COICOP_1999 | TYPE_OF_TRANSFORMATION | COUNTRY | FREQUENCY | IFS_FLAG | COMMON_REFERENCE_PERIOD | OVERLAP | SCALE | ACCESS_SHARING_LEVEL | SECURITY_CLASSIFICATION | TIME_PERIOD | value      | date       |
|------|------------|-------------|------------------------|---------|-----------|----------|-------------------------|---------|-------|----------------------|-------------------------|-------------|------------|------------|
| 0    | CPI        | \_T         | IX                     | NLD     | M         | true     | 2015A                   | OL      | 0     | PUBLIC_OPEN          | PUB                     | 1960-M04    | 15.805480  | 1960-04-30 |
| 1    | CPI        | \_T         | IX                     | NLD     | M         | true     | 2015A                   | OL      | 0     | PUBLIC_OPEN          | PUB                     | 1960-M05    | 15.653500  | 1960-05-31 |
| 2    | CPI        | \_T         | IX                     | NLD     | M         | true     | 2015A                   | OL      | 0     | PUBLIC_OPEN          | PUB                     | 1960-M06    | 15.501520  | 1960-06-30 |
| 3    | CPI        | \_T         | IX                     | NLD     | M         | true     | 2015A                   | OL      | 0     | PUBLIC_OPEN          | PUB                     | 1960-M07    | 15.501520  | 1960-07-31 |
| 4    | CPI        | \_T         | IX                     | NLD     | M         | true     | 2015A                   | OL      | 0     | PUBLIC_OPEN          | PUB                     | 1960-M08    | 15.349550  | 1960-08-31 |
| ...  | ...        | ...         | ...                    | ...     | ...       | ...      | ...                     | ...     | ...   | ...                  | ...                     | ...         | ...        | ...        |
| 1626 | CPI        | \_T         | IX                     | USA     | M         | true     | 2010A                   | OL      | 0     | PUBLIC_OPEN          | PUB                     | 2025-M03    | 146.659451 | 2025-03-31 |
| 1627 | CPI        | \_T         | IX                     | USA     | M         | true     | 2010A                   | OL      | 0     | PUBLIC_OPEN          | PUB                     | 2025-M04    | 147.116216 | 2025-04-30 |
| 1628 | CPI        | \_T         | IX                     | USA     | M         | true     | 2010A                   | OL      | 0     | PUBLIC_OPEN          | PUB                     | 2025-M05    | 147.423477 | 2025-05-31 |
| 1629 | CPI        | \_T         | IX                     | USA     | M         | true     | 2010A                   | OL      | 0     | PUBLIC_OPEN          | PUB                     | 2025-M06    | 147.926101 | 2025-06-30 |
| 1630 | CPI        | \_T         | IX                     | USA     | M         | true     | 2010A                   | OL      | 0     | PUBLIC_OPEN          | PUB                     | 2025-M07    | 148.149439 | 2025-07-31 |

<p>1631 rows × 14 columns</p>
</div>

</div>

You should get a tidy DataFrame with monthly series for both USA and
NLD.

------------------------------------------------------------------------

## WEO: download published data

WEO identifiers differ from CPI. If you already know the selector
pattern, you can pass a compact key directly:

``` python
weo = idata.retrieval.imfdata_by_key(dataset="WEO", key="USA+NLD.LUR.A")  # LUR = unemployment rate, A = annual
weo
```

<div>

<div>

|     | INDICATOR | COUNTRY | FREQUENCY | LATEST_ACTUAL_ANNUAL_DATA | OVERLAP | SCALE | METHODOLOGY_NOTES                                 | TIME_PERIOD | value | date       |
|-----|-----------|---------|-----------|---------------------------|---------|-------|---------------------------------------------------|-------------|-------|------------|
| 0   | LUR       | NLD     | A         | 2024                      | OL      | 0     | Source: National Statistics Office Latest actu... | 1980        | 3.354 | 1980-12-31 |
| 1   | LUR       | NLD     | A         | 2024                      | OL      | 0     | Source: National Statistics Office Latest actu... | 1981        | 4.583 | 1981-12-31 |
| 2   | LUR       | NLD     | A         | 2024                      | OL      | 0     | Source: National Statistics Office Latest actu... | 1982        | 6.525 | 1982-12-31 |
| 3   | LUR       | NLD     | A         | 2024                      | OL      | 0     | Source: National Statistics Office Latest actu... | 1983        | 8.254 | 1983-12-31 |
| 4   | LUR       | NLD     | A         | 2024                      | OL      | 0     | Source: National Statistics Office Latest actu... | 1984        | 8.090 | 1984-12-31 |
| ... | ...       | ...     | ...       | ...                       | ...     | ...   | ...                                               | ...         | ...   | ...        |
| 97  | LUR       | USA     | A         | 2024                      | OL      | 0     | Source: National Statistics Office Latest actu... | 2026        | 4.151 | 2026-12-31 |
| 98  | LUR       | USA     | A         | 2024                      | OL      | 0     | Source: National Statistics Office Latest actu... | 2027        | 4.079 | 2027-12-31 |
| 99  | LUR       | USA     | A         | 2024                      | OL      | 0     | Source: National Statistics Office Latest actu... | 2028        | 3.929 | 2028-12-31 |
| 100 | LUR       | USA     | A         | 2024                      | OL      | 0     | Source: National Statistics Office Latest actu... | 2029        | 3.801 | 2029-12-31 |
| 101 | LUR       | USA     | A         | 2024                      | OL      | 0     | Source: National Statistics Office Latest actu... | 2030        | 3.759 | 2030-12-31 |

<p>102 rows × 10 columns</p>
</div>

</div>

------------------------------------------------------------------------

## WEO_LIVE: download the live feed (requires auth)

``` python
weo_live = idata.retrieval.imfdata_by_key(
    dataset="WEO_LIVE",
    key="USA+NLD.LUR.A",
    needs_auth=True
)
```

As this data is confidential, we don’t display it here.

If you get an auth error, confirm your credentials/tokens and that your
environment exposes them (e.g., via env vars or a config file).

------------------------------------------------------------------------

## Codelists & subcodelists (for labels and mapping)

Discover the human-readable labels for codes by pulling **codelists**:

``` python
codelists = idata.metadata.get_codelists(dataset="CPI")
codelists
```

<div>

<div>

|     | codelist_id        | name                                  | version | n_codes |
|-----|--------------------|---------------------------------------|---------|---------|
| 0   | GF049              |                                       | None    | 1       |
| 1   | GF048              |                                       | None    | 1       |
| 2   | GF047              |                                       | None    | 1       |
| 3   | GF046              |                                       | None    | 1       |
| 4   | GF045              |                                       | None    | 1       |
| ... | ...                | ...                                   | ...     | ...     |
| 121 | CL_DERIVATION_TYPE | Derivation Type                       | 1.2.1   | 12      |
| 122 | CL_CONF_STATUS     | Confidentiality Status                | 1.0.0   | 12      |
| 123 | CL_COMMODITY       | Commodity                             | 2.2.0   | 135     |
| 124 | CL_GFS_STO         | GFS Stocks, Transactions, Other Flows | 2.9.0   | 389     |
| 125 | CL_CIVIL_STATUS    | Civil (or Marital) Status             | 1.0.1   | 8       |

<p>126 rows × 4 columns</p>
</div>

</div>

Drill down to a specific codelist:

``` python
dept = idata.metadata.get_subcodelist(dataset="CPI", codelist_id="CL_DEPARTMENT")
dept
```

    (   code_id                                               name description
     0      AFR                           African Department (AFR)            
     1      APD                  Asia and Pacific Department (APD)            
     2      COM                    Communications Department (COM)            
     3      CSF  Corporate Services and Facilities Department (...            
     4      DMD       Office of the Deputy Managing Director (DMD)            
     5      ETO                                Ethics Office (ETO)            
     6      EUO                            Offices in Europe (EUO)            
     7      EUR                          European Department (EUR)            
     8      FAD                    Fiscal Affairs Department (FAD)            
     9      FED           Fund Office of Executive Directors (FED)            
     10     FIN                           Finance Department (FIN)            
     11     GRC                 Grievance Committee Chairman (GRC)            
     12     HRD                   Human Resources Department (HRD)            
     13     ICD           Institute for Capacity Development (ICD)            
     14     IEO                Independent Evaluation Office (IEO)            
     15     INV                            Investment Office (INV)            
     16     ITD            Information Technology Department (ITD)            
     17     LEG                             Legal Department (LEG)            
     18     MCD      Middle East and Central Asia Department (MCD)            
     19     MCM      Monetary and Capital Markets Department (MCM)            
     20     MDT                             Mediation Office (MDT)            
     21     OAP     Regional Office for Asia and the Pacific (OAP)            
     22     OBP                Office of Budget and Planning (OBP)            
     23     OIA                     Office of Internal Audit (OIA)            
     24     OMB                                 Ombudsperson (OMB)            
     25     OMD              Office of the Managing Director (OMD)            
     26     ORM                    Office of Risk Management (ORM)            
     27     OII            Office of Internal Investigations (OII)            
     28     RES                          Research Department (RES)            
     29     SEC                       Secretary's Department (SEC)            
     30     SPR      Strategy, Policy, and Review Department (SPR)            
     31     STA                        Statistics Department (STA)            
     32     WHD                Western Hemisphere Department (WHD)            
     33     TRM          Office of Transformation Management (TRM)            ,
     DimensionEnv(African_Department_AFR='AFR', Asia_and_Pacific_Department_APD='APD', Communications_Department_COM='COM', Corporate_Services_and_Facilities_Department_CSF='CSF', Office_of_the_Deputy_Managing_Director_DMD='DMD', Ethics_Office_ETO='ETO', Offices_in_Europe_EUO='EUO', European_Department_EUR='EUR', Fiscal_Affairs_Department_FAD='FAD', Fund_Office_of_Executive_Directors_FED='FED', Finance_Department_FIN='FIN', Grievance_Committee_Chairman_GRC='GRC', Human_Resources_Department_HRD='HRD', Institute_for_Capacity_Development_ICD='ICD', Independent_Evaluation_Office_IEO='IEO', Investment_Office_INV='INV', Information_Technology_Department_ITD='ITD', Legal_Department_LEG='LEG', Middle_East_and_Central_Asia_Department_MCD='MCD', Monetary_and_Capital_Markets_Department_MCM='MCM', Mediation_Office_MDT='MDT', Regional_Office_for_Asia_and_the_Pacific_OAP='OAP', Office_of_Budget_and_Planning_OBP='OBP', Office_of_Internal_Audit_OIA='OIA', Ombudsperson_OMB='OMB', Office_of_the_Managing_Director_OMD='OMD', Office_of_Risk_Management_ORM='ORM', Office_of_Internal_Investigations_OII='OII', Research_Department_RES='RES', Secretary_s_Department_SEC='SEC', Strategy_Policy_and_Review_Department_SPR='SPR', Statistics_Department_STA='STA', Western_Hemisphere_Department_WHD='WHD', Office_of_Transformation_Management_TRM='TRM'))

Use these to build lookup tables for reporting or to validate
selections.

------------------------------------------------------------------------

## Tips & troubleshooting

- **Autocomplete is your friend:** Use `get_dimension_env(...)` so your
  IDE helps you select valid items.
- If exporting to GitHub README (GFM), render this doc with `--to gfm`
  and prefer `DataFrame.to_markdown(...)` inside chunks to get pure
  Markdown tables.

------------------------------------------------------------------------

## Minimal end-to-end example (CPI, monthly, All Items)

``` python
import imfidata as idata

# Discover dimensions
_ = idata.metadata.get_dimension_names("CPI")

# Build dim envs (with autocomplete)
indexes_df, indexes    = idata.metadata.get_subcodelist("CPI",dimenvs.INDEX_TYPE )
coicops_df,coicops    = idata.metadata.get_subcodelist("CPI", dimenvs.COICOP_1999)
transforms_df,transforms = idata.metadata.get_subcodelist("CPI", dimenvs.TYPE_OF_TRANSFORMATION)

# Assemble key
key = [
    ["USA","NLD"],
    [indexes.Consumer_price_index_CPI],
    [coicops.All_Items],
    [transforms.Index],
    ["M"]
]
keystr = idata.utils.make_key_str(key)

# Retrieve
cpi = idata.retrieval.imfdata_by_key(dataset="CPI", key=keystr)
cpi.head()
```

<div>

<div>

|     | INDEX_TYPE | COICOP_1999 | TYPE_OF_TRANSFORMATION | COUNTRY | FREQUENCY | IFS_FLAG | COMMON_REFERENCE_PERIOD | OVERLAP | SCALE | ACCESS_SHARING_LEVEL | SECURITY_CLASSIFICATION | TIME_PERIOD | value    | date       |
|-----|------------|-------------|------------------------|---------|-----------|----------|-------------------------|---------|-------|----------------------|-------------------------|-------------|----------|------------|
| 0   | CPI        | \_T         | IX                     | NLD     | M         | true     | 2015A                   | OL      | 0     | PUBLIC_OPEN          | PUB                     | 1960-M04    | 15.80548 | 1960-04-30 |
| 1   | CPI        | \_T         | IX                     | NLD     | M         | true     | 2015A                   | OL      | 0     | PUBLIC_OPEN          | PUB                     | 1960-M05    | 15.65350 | 1960-05-31 |
| 2   | CPI        | \_T         | IX                     | NLD     | M         | true     | 2015A                   | OL      | 0     | PUBLIC_OPEN          | PUB                     | 1960-M06    | 15.50152 | 1960-06-30 |
| 3   | CPI        | \_T         | IX                     | NLD     | M         | true     | 2015A                   | OL      | 0     | PUBLIC_OPEN          | PUB                     | 1960-M07    | 15.50152 | 1960-07-31 |
| 4   | CPI        | \_T         | IX                     | NLD     | M         | true     | 2015A                   | OL      | 0     | PUBLIC_OPEN          | PUB                     | 1960-M08    | 15.34955 | 1960-08-31 |

</div>

</div>
