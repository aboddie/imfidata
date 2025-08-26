from __future__ import annotations

import xml.etree.ElementTree as ET
from typing import Iterable, List, Tuple

import pandas as pd
import sdmx
from sdmx import Resource

from . import auth
from .sdmx_client import get_client
from .utils import make_env_from_pairs

# ---------- Dataflow / dataset registry ----------

def show_imf_datasets(needs_auth: bool = False) -> pd.DataFrame:
    """
    Fetches the IMF SDMX Dataflow registry and returns a DataFrame:
    columns: id, version, agencyID, name
    """
    client = get_client()
    rows = []
    for dataset in client.dataflow().iter_objects():
        if isinstance(dataset, sdmx.model.v21.DataflowDefinition):
            rows.append(
            {
                "id": dataset.id,
                "version": dataset.version,
                "agencyID": dataset.maintainer,
                "name_en": dataset.name,
            }
            )
    return pd.DataFrame(rows, columns=["id", "version", "agencyID", "name_en"])


# ---------- DSD helpers ----------

def _get_dsd(dataset: str) -> sdmx.message.StructureMessage:
    client = get_client()
    dsd_id = f"DSD_{dataset}"
    return client.datastructure(dsd_id, params=dict(references="descendants"))


def get_dimension_names_old(dataset: str) -> pd.DataFrame:
    """
    Return dimension names for a dataset as a DataFrame with one column "Dimension".
    """
    client = get_client()
    dsd_id = f"DSD_{dataset}"
    msg = client.get(resource_type=Resource.datastructure, resource_id=dsd_id)
    descriptor = msg.dataflow[0].structure.dimensions
    dim_list = sdmx.to_pandas(descriptor)
    return pd.DataFrame(dim_list, columns=["Dimension"])

def resolve_codelist(ds_msg, component):
    # 1) local representation
    lr = getattr(component, "local_representation", None)
    enum_ref = getattr(lr, "enumerated", None) if lr else None
    if enum_ref and getattr(enum_ref, "id", None) in ds_msg.codelist:
        return ds_msg.codelist[enum_ref.id]
    # 2) concept's core representation
    concept = getattr(component, "concept_identity", None)
    cr = getattr(concept, "core_representation", None) if concept else None
    enum_ref = getattr(cr, "enumerated", None) if cr else None
    if enum_ref and getattr(enum_ref, "id", None) in ds_msg.codelist:
        return ds_msg.codelist[enum_ref.id]
    # 3) heuristic CL_<DIM_ID>
    guess_id = f"CL_{component.id}"
    if guess_id in ds_msg.codelist:
        return ds_msg.codelist[guess_id]
    return None

def _fetch_dsd_message(flow_id: str) -> sdmx.message.StructureMessage:
    """Fetch a StructureMessage that includes the DSD + codelists for a flow."""
    cl = get_client()
    # First try resolving the actual DSD ID via dataflow (handles agency/versioned IDs)
    try:
        df_msg = cl.dataflow(flow_id, params={"references": "all"})
        dsd_ref = df_msg.dataflow[flow_id].structure
        dsd_id = getattr(dsd_ref, "id", None) or f"DSD_{flow_id}"
    except Exception:
        dsd_id = f"DSD_{flow_id}"
    # Fetch with descendants so codelists are included
    return cl.datastructure(dsd_id, params={"references": "descendants"})

def _extract_dsd(struct_msg, preferred_id: str = None):
    """Return a DataStructureDefinition from a StructureMessage, robustly."""
    for attr in ("metadatastructure", "datastructure", "structure", "_metadatastructure", "_datastructure"):
        container = getattr(struct_msg, attr, None)
        if isinstance(container, dict) and container:
            if preferred_id and preferred_id in container:
                return container[preferred_id]
            return next(iter(container.values()))
    # Fallback: scan all objects
    for obj in struct_msg.iter_objects():
        if obj.__class__.__name__.endswith("DataStructureDefinition"):
            return obj
    raise RuntimeError("No DataStructureDefinition found in StructureMessage.")

def get_dimension_names(dataset: str) -> pd.DataFrame:
    """
    Return a DataFrame with two columns:
      - dimension: the dimension ID
      - codelists: the codelist ID if available, else None
    """
    msg = _fetch_dsd_message(dataset)
    # Prefer DSD_<FLOW> as the key if present
    preferred_id = f"DSD_{dataset}"
    dsd = _extract_dsd(msg, preferred_id=preferred_id)

    rows = []
    for dim in dsd.dimensions.components:
        cl = resolve_codelist(msg, dim)
        rows.append({"dimension": dim.id, "codelists": getattr(cl, "id", None)})

    return pd.DataFrame(rows, columns=["dimension", "codelists"])
def get_dimension_values(dataset: str, dimension: str) -> pd.DataFrame:
    """
    Return codes for a dimension as DataFrame with columns ["code", "name"].
    Now correctly retrieves the codelist referenced by the dimension in the DSD.
    """
    ds = _get_dsd(dataset)
    dsd = ds.datastructure[dataset]  # Get the actual DSD object

    # Find the dimension
    dim = dsd.structure.dimensions.get(dimension)
    if not dim:
        raise ValueError(f"Dimension '{dimension}' not found in DSD_{dataset}")

    # Get the codelist via the dimension's representation
    codelist_ref = dim.local_representation.enumerated
    if not codelist_ref:
        raise ValueError(f"Dimension '{dimension}' has no associated codelist")

    # Resolve the codelist from the message
    cl = ds.codelist[codelist_ref.id]
    rows = [{"code": code.id, "name": str(code.name)} for code in cl.items]
    return pd.DataFrame(rows, columns=["code", "name"])

def get_dimension_values_old(dataset: str, dimension: str, addcl: bool = True) -> pd.DataFrame:
    """
    Return codes for a dimension as DataFrame with columns ["code", "name"].
    """
    ds = _get_dsd(dataset)
    cl_id = f"CL_{dimension}" if addcl and not dimension.startswith("CL_") else dimension
    cl = ds.codelist[cl_id]
    rows = [{"code": code.id, "name": str(getattr(code, "name", ""))} for code in cl]
    return pd.DataFrame(rows, columns=["code", "name"])


def get_dimension_values_env(codelist: str, dimension: str) ->  DimensionEnv:
    """
    Return  the DataFrame 

    """
    ds = _get_dsd(dataset)
    cl_id = f"CL_{dimension}" if addcl and not dimension.startswith("CL_") else dimension
    cl = ds.codelist[cl_id]

    rows = [{"code": code.id, "name": str(getattr(code, "name", ""))} for code in cl]
    #df = pd.DataFrame(rows, columns=["code", "name"])
    env = make_env_from_pairs((r["name"], r["code"]) for r in rows)
    return  env

def get_dimension_values_and_env(dataset: str, dimension: str, addcl: bool = True) -> Tuple[pd.DataFrame, DimensionEnv]:
    """
    Convenience: return both the DataFrame and a dot-accessible env built from it.
    Avoids a second fetch and re-parsing.
    """
    ds = _get_dsd(dataset)
    cl_id = f"CL_{dimension}" if addcl and not dimension.startswith("CL_") else dimension
    cl = ds.codelist[cl_id]

    rows = [{"code": code.id, "name": str(getattr(code, "name", ""))} for code in cl]
    df = pd.DataFrame(rows, columns=["code", "name"])
    env = make_env_from_pairs((r["name"], r["code"]) for r in rows)
    return  df, env

def get_dimension_name_env(dataset: str):
    """
    Convenience: build a dot-accessible env mapping
    """
    df = get_dimension_names(dataset)
    pairs: Iterable[Tuple[str, str]] = [(row["dimension"], row["codelists"]) for _, row in df.iterrows()]
    return make_env_from_pairs(pairs)



def get_dimension_env(dataset: str, dimension: str):
    """
    Convenience: build a dot-accessible env mapping sanitized labels to codes.
    """
    df = get_dimension_values(dataset, dimension)
    pairs: Iterable[Tuple[str, str]] = [(row["name"], row["code"]) for _, row in df.iterrows()]
    return make_env_from_pairs(pairs)


def get_codelists(dataset: str) -> pd.DataFrame:
    """
    Return summary of all codelists in the dataset DSD.
    Columns: codelist_id, name, version, n_codes
    """
    sm = _get_dsd(dataset)
    rows = []
    for cl_id, cl in sm.codelist.items():
        rows.append(
            {
                "codelist_id": cl_id,
                "name": str(getattr(cl, "name", "")),
                "version": str(getattr(cl, "version", "")),
                "n_codes": len(cl),
            }
        )
    return pd.DataFrame(rows, columns=["codelist_id", "name", "version", "n_codes"])


def get_subcodelist(dataset: str, codelist_id: str) -> pd.DataFrame:
    """
    Return the codes for a single codelist as DataFrame with columns:
    code_id, name, description
    """
    sm = _get_dsd(dataset)
    cl = sm.codelist[codelist_id]
    rows = []
    for code in cl:
        rows.append(
            {
                "code_id": code.id,
                "name": str(getattr(code, "name", "")),
                "description": str(getattr(code, "description", "")),
            }
        )
    df= pd.DataFrame(rows, columns=["code_id", "name", "description"])
    pairs: Iterable[Tuple[str, str]] = [(row["name"], row["code_id"]) for _, row in df.iterrows()]
    myenv= make_env_from_pairs(pairs)
    return df,myenv
