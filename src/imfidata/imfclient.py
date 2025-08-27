from __future__ import annotations

from functools import lru_cache
from typing import List, Tuple

import pandas as pd
import sdmx

from .auth import get_request_header
from .utils import make_env_from_df, make_env_from_pairs, convert_time_period_auto

class IMFClient():

    __slots__ = ["_client", "_headers", "authenticated"]

    def __init__(self, authentication: bool = False):
        self._client = sdmx.Client("IMF_DATA")
        self._headers = get_request_header(authentication)
        self.authenticated = authentication

    def authenticate(self):
        '''
        Obtain a bearer token and include Authorization header in future requests.
        '''
        self._headers = get_request_header(True)
        self.authenticated = True

    def remove_authentication(self):
        '''
        Remove Authorization header from future requests.
        '''
        self._headers = get_request_header(False)
        self.authenticated = False

    def __str__(self) -> str:
        if self.authenticated:
            return f"Authenticated connection to data.imf.org."
        else:
            return f"Unauthenticated connection to data.imf.org."
           
    def show_imf_datasets(self) -> pd.DataFrame:
        """
        Fetches all IMF datasets and returns a DataFrame:
        columns: id, version, agencyID, name_en
        """
        rows = []
        for dataset in self._client.dataflow(headers=self._headers).iter_objects():
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

    @lru_cache(maxsize=10)
    def _get_dsd_msg(self, dsd_id: str) -> sdmx.message.StructureMessage:
        # TODO: add agency and version parameters
        return self._client.datastructure(dsd_id, params=dict(references="descendants"), headers=self._headers)
    
    @lru_cache(maxsize=10)
    def _get_dsd_from_dataflow(self, flow_id: str) -> sdmx.model.v21.DataStructureDefinition:
        # TODO: add agency and version parameters
        df_msg = self._client.dataflow(flow_id, headers=self._headers)
        return df_msg.dataflow[flow_id].structure
    
    @lru_cache(maxsize=10)
    def _get_codelist(self, codelist_id: str) -> sdmx.model.common.Codelist:
        # TODO: add agency and version parameters
        return self._client.codelist(codelist_id, headers=self._headers).codelist[0]
    
    def _get_list_of_dimension_values(self, dataset: str, dimension: str) -> List[Tuple[str, str]]:
        # TODO: add agency and version parameters
        dsd = self._get_dsd_from_dataflow(dataset)

        # Find the dimension
        try:
            dim = dsd.dimensions.get(dimension)
        except KeyError:
            raise ValueError(f"Dimension '{dimension}' not found in {dataset}'s DSD. Available dimensions: {[d.id for d in dsd.dimensions.components]}")
        conceptIdentity = dim.concept_identity
        codelist = conceptIdentity.core_representation.enumerated
        if codelist is not None:
            return [{"code": code.id, "name": str(code.name)} for code in codelist.items.values()]
        else:
            raise ValueError(f"Dimension '{dimension}' has no associated codelist")
    
    def get_dimension_values(self, dataset: str, dimension: str) -> pd.DataFrame:
        '''
        Return a DataFrame with columns 'code' and 'name' for the specified dimension.
        '''
        rows = self._get_list_of_dimension_values(dataset, dimension)
        return pd.DataFrame(rows, columns=["code", "name"])
    
    def get_dimension_values_env(self, dataset: str, dimension: str) -> dict:
        '''
        Return a dot-accessible env mapping sanitized labels to codes for the specified dimension.
        '''
        rows = self._get_list_of_dimension_values(dataset, dimension)
        return make_env_from_pairs((r["name"], r["code"]) for r in rows)

    def get_dimension_names(self, dataset: str) -> pd.DataFrame:
        """
        Return a DataFrame with two columns:
        - dimension: the dimension ID
        - codelists: the codelist ID if available, else None
        """
        dsd = self._get_dsd_from_dataflow(dataset)

        rows = []
        for dim in dsd.dimensions.components:
            conceptIdentity = dim.concept_identity
            codelist = conceptIdentity.core_representation.enumerated
            if codelist is not None:
                cl_id = codelist.id
            else:
                cl_id = None
            rows.append({"dimension": dim.id, "codelists": cl_id})
        return pd.DataFrame(rows, columns=["dimension", "codelists"])
    
    def get_dimension_names_env(self, dataset: str):
        """
        Convenience: build a dot-accessible env mapping
        """
        return make_env_from_df(self.get_dimension_names(dataset),"dimension", "codelists")

    def get_codelist(self, codelist_id: str) -> pd.DataFrame:
        """
        Return the codes for a single codelist as DataFrame with columns:
        code_id, name, description
        """
        cl = self._get_codelist(codelist_id)
        rows = []
        for code in cl.items.values():
            rows.append(
                {
                    "code_id": code.id,
                    "name": code.name,
                    "description": code.description,
                }
            )
        return pd.DataFrame(rows, columns=["code_id", "name", "description"])

    def get_codelist_env(self, codelist_id: str) -> pd.DataFrame:
        return make_env_from_df(self.get_codelist(codelist_id), "code_id", "name")
    
    def get_codelists(self, dataset: str) -> pd.DataFrame:
        """
        Return summary of all codelists in the dataset DSD.
        Columns: codelist_id, name, version, n_codes
        """
        dsd = self._get_dsd_from_dataflow(dataset)
        #TODO cleanup
        sm = self._get_dsd_msg(dsd.id)
        rows = []
        for cl in sm.codelist.items().values():
            rows.append(
                {
                    "codelist_id": cl.id,
                    "name": cl.name,
                    "version": cl.version,
                    "n_codes": len(cl),
                }
            )
        return pd.DataFrame(rows, columns=["codelist_id", "name", "version", "n_codes"])
    
    def imfdata_by_key(self, dataset: str, key: str, params: dict = {}, convert_dates: bool = True) -> pd.DataFrame:
        """
        Fetches SDMX data and returns a pandas DataFrame.

        Args:
        resource_id: SDMX resource identifier (e.g. 'IMF.RES,WEO')
        key:         key string (e.g. 'USA+CAN.LUR.A')
        params:      dict of query params (e.g. {'startPeriod': 2018})
        convert_dates: if True, converts TIME_PERIOD to 'date' at end of period.

        Returns:
        pandas.DataFrame of the time series.
        """
        try:
            df= sdmx.to_pandas(self._client.data(
                resource_id=dataset,
                key=key,
                params=params,
                headers=self._headers
            ))
            df = df.reset_index()
            if convert_dates:
                df = convert_time_period_auto(df, time_col='TIME_PERIOD', out_col='date')
            return df
        except Exception as e:
            raise RuntimeError(f"Error fetching and converting {dataset}: {e}")
