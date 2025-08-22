# iData


## Why this tutorial?

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

### 1. Install

``` python
# If you don't have imfidata yet, uncomment and run:
# Installation instructions to follow
# %pip install imfidata
```

### 2. Import

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
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }
&#10;    .dataframe tbody tr th {
        vertical-align: top;
    }
&#10;    .dataframe thead th {
        text-align: right;
    }
</style>

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
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }
&#10;    .dataframe tbody tr th {
        vertical-align: top;
    }
&#10;    .dataframe thead th {
        text-align: right;
    }
</style>

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
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }
&#10;    .dataframe tbody tr th {
        vertical-align: top;
    }
&#10;    .dataframe thead th {
        text-align: right;
    }
</style>

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
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }
&#10;    .dataframe tbody tr th {
        vertical-align: top;
    }
&#10;    .dataframe thead th {
        text-align: right;
    }
</style>

|     | id      | version | agencyID    | name_en                                           |
|-----|---------|---------|-------------|---------------------------------------------------|
| 0   | AFRREO  | 6.0.1   | IMF.AFR     | Sub-Saharan Africa Regional Economic Outlook (... |
| 1   | FSI     | 3.0.1   | IMF.RES     | Financial Stress Index (FSI)                      |
| 2   | MFS_ODC | 9.0.1   | IMF.STA     | Monetary and Financial Statistics (MFS), Other... |
| 3   | PIP     | 4.0.0   | IMF.STA     | Portfolio Investment Positions by Counterpart ... |
| 4   | GDS     | 2.0.0   | IMF.RES.GDS | Global Data Source (GDS)                          |
| ... | ...     | ...     | ...         | ...                                               |
| 80  | SRD     | 1.0.0   | IMF.RES     | Structural Reform Database (SRD)                  |
| 81  | BOP     | 21.0.0  | IMF.STA     | Balance of Payments (BOP)                         |
| 82  | QGFS    | 11.0.0  | IMF.STA     | Quarterly Government Finance Statistics (QGFS)    |
| 83  | PI      | 2.0.0   | IMF.STA     | Production Indexes (PI)                           |
| 84  | CCI     | 3.0.0   | IMF.STA     | Climate Change Indicators (CCI)                   |

<p>85 rows × 4 columns</p>
</div>

</div>

``` python
weolive = mydatasets.query("id == 'WEO_LIVE'")
weolive
```

<div>

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }
&#10;    .dataframe tbody tr th {
        vertical-align: top;
    }
&#10;    .dataframe thead th {
        text-align: right;
    }
</style>

|     | id       | version | agencyID    | name_en                           |
|-----|----------|---------|-------------|-----------------------------------|
| 7   | WEO_LIVE | 3.0.0   | IMF.RES.WEO | World Economic Outlook (WEO) Live |

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
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }
&#10;    .dataframe tbody tr th {
        vertical-align: top;
    }
&#10;    .dataframe thead th {
        text-align: right;
    }
</style>

|     | Dimension   |
|-----|-------------|
| 0   | COUNTRY     |
| 1   | INDICATOR   |
| 2   | FREQ        |
| 3   | TIME_PERIOD |

</div>

</div>

### Example: CPI

``` python
dimensions = idata.metadata.get_dimension_names("CPI")
dimensions
```

<div>

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }
&#10;    .dataframe tbody tr th {
        vertical-align: top;
    }
&#10;    .dataframe thead th {
        text-align: right;
    }
</style>

|     | Dimension              |
|-----|------------------------|
| 0   | COUNTRY                |
| 1   | INDEX_TYPE             |
| 2   | COICOP_1999            |
| 3   | TYPE_OF_TRANSFORMATION |
| 4   | FREQ                   |
| 5   | TIME_PERIOD            |

</div>

</div>

You’ll see the dimension “names” you must populate when building a key
(e.g., country, indicator/index type, COICOP, transformation,
frequency).

------------------------------------------------------------------------

## Developer-friendly keys with autocompletion

Typing cryptic SDMX codes by hand is… not fun. `imfidata` can generate
Python “environments” that **autocomplete** descriptive names to the
right codes.

### Build an environment for a CPI dimension

``` python
indexes = idata.metadata.get_dimension_env("CPI", "INDEX_TYPE")
indexes
```

    DimensionEnv(Bank_stock_index='BSI', Core_consumer_price_index_CPI='CCPI', Core_consumer_price_index_CCPI_SVN='CCPISVN', Commodity_price_index_energy_crude_oil_petroleum='CECO', Commodity_net_export_price_index='CEMPI', Commodity_export_price_index='CEPI', Core_HICP_inflation_forecast='CHICPIF', Commodity_import_price_index='CMPI', Core_PCE_Price_Index='CPCE', Consumer_price_index_CPI='CPI', Relative_consumer_price_index_CPI='CPIR', Consumer_price_index_Urban='CPIU', Commodity_price_index='CPIX', Deflator='D', Flexible_exchange_market_pressure_index='DMN_EMP_CR_SQSCLD', Export_price_index_XPI='EPI', Financial_stress_indicators='FSI', Herfindahl_index='HFIDX', Harmonised_index_of_consumer_prices_HICP='HICP', Industrial_production_index_IPI='IPIX', Chain_linked_volume='L', Chain_linked_volume_rebased='LR', Import_price_index='MPI', Nominal_effective_exchange_rate_NEER='NEER', Price_deflator='PD', Producer_price_index_PPI='PPI', Real_effective_exchange_rate_REER='REER', Retail_sales_index='RSI', Financial_price_index='SQRMSCINC_RET_SQSCLD', Stock_returns='STKRET', Theil_index='THEIL', Terms_of_trade_TOT='TT', Volume_index='VI', Wholesale_price_index_WPI='WPI', Price_deflator_Eurostat='PDE', Unit_value_deflator='UVD', REER_ASM='REER_ASM', Core_producer_price_index_Core_PPI='CPPI', Purchasing_managers_index_PMI='PMI', Harmonised_index_of_producer_prices_HIPP='HIPP', Morgan_Stanley_MSCI_stock_price_index='FMSCI', Terms_of_trade_TOT_Goods='TTG', Price_deflator_EUR='PD_EUR', Price_deflator_USD='PD_USD', Price_deflator_SDR='PD_XDR', Production_index='PIX', Core_inflation_excluding_food_and_energy='CCPIXFEN', Core_inflation_including_housing='PCPIHACO', Consumer_price_index_CPI_common_reference_period='CPISRP')

Type `indexes.` in your editor and let autocomplete reveal options like
`Consumer_price_index_CPI`. Selecting it yields the correct code at
runtime.

``` python
coicops = idata.metadata.get_dimension_env("CPI", "COICOP_1999")
coicops
```

    DimensionEnv(Food_and_non_alcoholic_beverages='CP01', Alcoholic_beverages_tobacco_and_narcotics='CP02', Clothing_and_footwear='CP03', Housing_water_electricity_gas_and_other_fuels='CP04', Furnishings_household_equipment_and_routine_household_maintenance='CP05', Health='CP06', Transport='CP07', Communication='CP08', Recreation_and_culture='CP09', Education='CP10', Restaurants_and_hotels='CP11', Miscellaneous_goods_and_services='CP12', Individual_consumption_expenditure_of_non_profit_institutions_serving_households_NPISHs='CP13', Individual_consumption_expenditure_of_general_government='CP14', All_Items='_T')

### About transformation codes

\[The next issue needs to be fixed by STA. In dimensions we have
`CL_TYPE_OF_TRANSFORMATION` but in codelists we have
`CL_CPI_TYPE_OF_TRANSFORMATION`\]

``` python
transforms = idata.metadata.get_dimension_env("CPI", "CL_CPI_TYPE_OF_TRANSFORMATION")
transforms
```

    DimensionEnv(Index='IX', Period_average_Period_over_period_percent_change='POP_PCH_PA_PT', Period_average_Year_over_year_YOY_percent_change='YOY_PCH_PA_PT', Weight='WGT', Weight_Percent='WGT_PT', Standard_reference_period_2010_100_Index='SRP_IX', Standard_reference_period_2010_100_Period_average_Period_over_period_percent_change='SRP_POP_PCH_PA_PT', Standard_reference_period_2010_100_Period_average_Year_over_year_YOY_percent_change='SRP_YOY_PCH_PA_PT')

------------------------------------------------------------------------

## Build a CPI key (countries × index × COICOP × transform × freq)

**Rule of thumb:** Don’t pass raw strings when an environment is
available—use the autocompleted objects so you get valid codes. Also
make sure to put entries in a list–not as a string.

``` python
mycountries = ["USA", "NLD"]  # ISO3
myindexes   = [indexes.Consumer_price_index_CPI]
mycoicops   = [coicops.All_Items]
mytransforms= [transforms.Index]
myfreq      = ["M"]  # monthly

key = [mycountries, myindexes, mycoicops, mytransforms, myfreq]
keystr = idata.utils.make_key_str(key)
keystr
```

    'USA+NLD.CPI._T.IX.M'

`keystr` is your SDMX key string (e.g., `USA+NLD.CPI.ALL...M`)—compact
and valid.

------------------------------------------------------------------------

## Download CPI data

``` python
temp = idata.retrieval.imfdata_by_key(dataset="CPI", key=keystr)
temp
```

    xml.Reader got no structure=… argument for StructureSpecificData

<div>

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }
&#10;    .dataframe tbody tr th {
        vertical-align: top;
    }
&#10;    .dataframe thead th {
        text-align: right;
    }
</style>

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

You should get a tidy DataFrame with time series for both USA and NLD.
From here you can plot, resample, or export.

------------------------------------------------------------------------

## WEO: download published data

WEO identifiers differ from CPI. If you already know the selector
pattern, you can pass a compact key directly:

``` python
temp = idata.retrieval.imfdata_by_key(dataset="WEO", key="USA+NLD.LUR.A")
temp
```

    xml.Reader got no structure=… argument for StructureSpecificData

<div>

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }
&#10;    .dataframe tbody tr th {
        vertical-align: top;
    }
&#10;    .dataframe thead th {
        text-align: right;
    }
</style>

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

Here, `LUR` is the unemployment rate concept; `A` = annual.

------------------------------------------------------------------------

## WEO_LIVE: download the live feed (requires auth)

``` python
temp = idata.retrieval.imfdata_by_key(dataset="WEO_LIVE",
                                      key="USA+NLD.LUR.A",
                                      needs_auth=True)
temp
```

    xml.Reader got no structure=… argument for StructureSpecificData

<div>

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }
&#10;    .dataframe tbody tr th {
        vertical-align: top;
    }
&#10;    .dataframe thead th {
        text-align: right;
    }
</style>

|     | INDICATOR | COUNTRY | FREQUENCY | DESK_SERIES | OVERLAP | SCALE | TIME_PERIOD | value    | date       |
|-----|-----------|---------|-----------|-------------|---------|-------|-------------|----------|------------|
| 0   | LUR       | NLD     | A         | 138LUR      | OL      | 0     | 1980        | 3.354227 | 1980-12-31 |
| 1   | LUR       | NLD     | A         | 138LUR      | OL      | 0     | 1981        | 4.583473 | 1981-12-31 |
| 2   | LUR       | NLD     | A         | 138LUR      | OL      | 0     | 1982        | 6.524656 | 1982-12-31 |
| 3   | LUR       | NLD     | A         | 138LUR      | OL      | 0     | 1983        | 8.254443 | 1983-12-31 |
| 4   | LUR       | NLD     | A         | 138LUR      | OL      | 0     | 1984        | 8.089701 | 1984-12-31 |
| ... | ...       | ...     | ...       | ...         | ...     | ...   | ...         | ...      | ...        |
| 127 | LUR       | USA     | A         | 111LUR      | OL      | 0     | 2026        | 4.299424 | 2026-12-31 |
| 128 | LUR       | USA     | A         | 111LUR      | OL      | 0     | 2027        | 4.023825 | 2027-12-31 |
| 129 | LUR       | USA     | A         | 111LUR      | OL      | 0     | 2028        | 3.860212 | 2028-12-31 |
| 130 | LUR       | USA     | A         | 111LUR      | OL      | 0     | 2029        | 3.746141 | 2029-12-31 |
| 131 | LUR       | USA     | A         | 111LUR      | OL      | 0     | 2030        | 3.700654 | 2030-12-31 |

<p>132 rows × 9 columns</p>
</div>

</div>

If you get an auth error, confirm your credentials/tokens and that your
environment exposes them (e.g., via env vars or a config file).

------------------------------------------------------------------------

## Codelists & subcodelists (for labels and mapping)

Want to discover the human-readable labels for codes? Pull the
**codelists**:

``` python
temp = idata.metadata.get_codelists(dataset="CPI")
temp
```

<div>

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }
&#10;    .dataframe tbody tr th {
        vertical-align: top;
    }
&#10;    .dataframe thead th {
        text-align: right;
    }
</style>

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
temp = idata.metadata.get_subcodelist(dataset="CPI", codelist_id="CL_DEPARTMENT")
temp
```

<div>

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }
&#10;    .dataframe tbody tr th {
        vertical-align: top;
    }
&#10;    .dataframe thead th {
        text-align: right;
    }
</style>

|     | code_id | name                                              | description |
|-----|---------|---------------------------------------------------|-------------|
| 0   | AFR     | African Department (AFR)                          |             |
| 1   | APD     | Asia and Pacific Department (APD)                 |             |
| 2   | COM     | Communications Department (COM)                   |             |
| 3   | CSF     | Corporate Services and Facilities Department (... |             |
| 4   | DMD     | Office of the Deputy Managing Director (DMD)      |             |
| 5   | ETO     | Ethics Office (ETO)                               |             |
| 6   | EUO     | Offices in Europe (EUO)                           |             |
| 7   | EUR     | European Department (EUR)                         |             |
| 8   | FAD     | Fiscal Affairs Department (FAD)                   |             |
| 9   | FED     | Fund Office of Executive Directors (FED)          |             |
| 10  | FIN     | Finance Department (FIN)                          |             |
| 11  | GRC     | Grievance Committee Chairman (GRC)                |             |
| 12  | HRD     | Human Resources Department (HRD)                  |             |
| 13  | ICD     | Institute for Capacity Development (ICD)          |             |
| 14  | IEO     | Independent Evaluation Office (IEO)               |             |
| 15  | INV     | Investment Office (INV)                           |             |
| 16  | ITD     | Information Technology Department (ITD)           |             |
| 17  | LEG     | Legal Department (LEG)                            |             |
| 18  | MCD     | Middle East and Central Asia Department (MCD)     |             |
| 19  | MCM     | Monetary and Capital Markets Department (MCM)     |             |
| 20  | MDT     | Mediation Office (MDT)                            |             |
| 21  | OAP     | Regional Office for Asia and the Pacific (OAP)    |             |
| 22  | OBP     | Office of Budget and Planning (OBP)               |             |
| 23  | OIA     | Office of Internal Audit (OIA)                    |             |
| 24  | OMB     | Ombudsperson (OMB)                                |             |
| 25  | OMD     | Office of the Managing Director (OMD)             |             |
| 26  | ORM     | Office of Risk Management (ORM)                   |             |
| 27  | OII     | Office of Internal Investigations (OII)           |             |
| 28  | RES     | Research Department (RES)                         |             |
| 29  | SEC     | Secretary's Department (SEC)                      |             |
| 30  | SPR     | Strategy, Policy, and Review Department (SPR)     |             |
| 31  | STA     | Statistics Department (STA)                       |             |
| 32  | WHD     | Western Hemisphere Department (WHD)               |             |
| 33  | TRM     | Office of Transformation Management (TRM)         |             |

</div>

</div>

Use these to build lookup tables for reporting or to validate
selections.

------------------------------------------------------------------------

## Tips & troubleshooting

- **Autocomplete is your friend:** Use `make_dimension_env` so your IDE
  helps you select valid items.

------------------------------------------------------------------------

## Minimal end-to-end example (CPI, monthly, All Items)

``` python
import imfidata as idata

# Discover dimensions
_ = idata.metadata.get_dimension_names("CPI")

# Build dim envs (with autocomplete)
indexes    = idata.metadata.get_dimension_env("CPI","INDEX_TYPE")
coicops    = idata.metadata.get_dimension_env("CPI","COICOP_1999")
transforms = idata.metadata.get_dimension_env("CPI","CL_CPI_TYPE_OF_TRANSFORMATION")  # or CL_TYPE_OF_TRANSFORMATION

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

    xml.Reader got no structure=… argument for StructureSpecificData

<div>

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }
&#10;    .dataframe tbody tr th {
        vertical-align: top;
    }
&#10;    .dataframe thead th {
        text-align: right;
    }
</style>

|     | INDEX_TYPE | COICOP_1999 | TYPE_OF_TRANSFORMATION | COUNTRY | FREQUENCY | IFS_FLAG | COMMON_REFERENCE_PERIOD | OVERLAP | SCALE | ACCESS_SHARING_LEVEL | SECURITY_CLASSIFICATION | TIME_PERIOD | value    | date       |
|-----|------------|-------------|------------------------|---------|-----------|----------|-------------------------|---------|-------|----------------------|-------------------------|-------------|----------|------------|
| 0   | CPI        | \_T         | IX                     | NLD     | M         | true     | 2015A                   | OL      | 0     | PUBLIC_OPEN          | PUB                     | 1960-M04    | 15.80548 | 1960-04-30 |
| 1   | CPI        | \_T         | IX                     | NLD     | M         | true     | 2015A                   | OL      | 0     | PUBLIC_OPEN          | PUB                     | 1960-M05    | 15.65350 | 1960-05-31 |
| 2   | CPI        | \_T         | IX                     | NLD     | M         | true     | 2015A                   | OL      | 0     | PUBLIC_OPEN          | PUB                     | 1960-M06    | 15.50152 | 1960-06-30 |
| 3   | CPI        | \_T         | IX                     | NLD     | M         | true     | 2015A                   | OL      | 0     | PUBLIC_OPEN          | PUB                     | 1960-M07    | 15.50152 | 1960-07-31 |
| 4   | CPI        | \_T         | IX                     | NLD     | M         | true     | 2015A                   | OL      | 0     | PUBLIC_OPEN          | PUB                     | 1960-M08    | 15.34955 | 1960-08-31 |

</div>

</div>
