

# retrieval.py
from __future__ import annotations
from typing import Optional, Dict
import pandas as pd
import sdmx

from .sdmx_client import get_client
from . import auth
from . import utils

import os
import tempfile


def convert_time_period_auto(df, time_col='TIME_PERIOD', out_col='date'):
    """
    Convert a 'time_period' column to Python date objects at the END of the period.
    Supported formats (auto-detected):
      - Annual:    '1960'          -> 1960-12-31
      - Monthly:   '1960-M04'      -> 1960-04-30
      - Quarterly: '1960-Q2'       -> 1960-06-30
    Unrecognized formats are left as NaT.
    """
    s = df[time_col].astype(str)
    result = []  # List to collect end-of-period dates

    for val in s:
        val = val.strip()  # Remove whitespace
        try:
            if '-M' in val:
                # Monthly: '1960-M04'
                year_str, month_part = val.split('-M')
                if year_str.isdigit() and month_part.isdigit():
                    year = int(year_str)
                    month = int(month_part)
                    if 1 <= month <= 12:
                        # End of the given month
                        dt = pd.Timestamp(year=year, month=month, day=1) + pd.offsets.MonthEnd(1)
                        result.append(dt)
                        continue
            elif '-Q' in val:
                # Quarterly: '1960-Q2'
                year_str, q_part = val.split('-Q')
                if year_str.isdigit() and q_part.isdigit():
                    year = int(year_str)
                    quarter = int(q_part)
                    if 1 <= quarter <= 4:
                        month = quarter * 3  # Q1: Mar, Q2: Jun, Q3: Sep, Q4: Dec
                        dt = pd.Timestamp(year=year, month=month, day=1) + pd.offsets.MonthEnd(1)
                        result.append(dt)
                        continue
            elif val.isdigit() and len(val) == 4:
                # Annual: '1960' -> Dec 31
                year = int(val)
                result.append(pd.Timestamp(year=year, month=12, day=31))
                continue
        except Exception as e:
            pass  # If anything fails, fall through to NaT

        # If no match or error, append NaT
        result.append(pd.NaT)

    # Create a copy of the DataFrame and add the result as a datetime column
    df_copy = df.copy()
    df_copy[out_col] = pd.to_datetime(result)  # Ensures proper dtype
    return df_copy  # ✅ Critical: return the modified DataFrame


def imfdata_by_key(
    resource_id: str,
    key: str,
    params: dict = None,
    needs_auth: bool = True,
    convert_dates: bool = True
):
    """
    Fetches SDMX data and returns a pandas DataFrame.

    Args:
      resource_id: SDMX resource identifier (e.g. 'IMF.RES,WEO')
      key:         key string (e.g. 'USA+CAN.LUR.A')
      params:      dict of query params (e.g. {'startPeriod': 2018})
      needs_auth:  if True, obtains a bearer token and includes Authorization header.
      convert_dates: if True, converts TIME_PERIOD to 'date' at end of period.

    Returns:
      pandas.DataFrame of the time series.
    """
    headers = {"User-Agent": "idata-script-client"}

    if needs_auth:
        token_resp = auth.acquire_access_token()
        token_type = token_resp.get("token_type", "Bearer")
        access_token = token_resp["access_token"]
        headers["Authorization"] = f"{token_type} {access_token}"

    client = sdmx.Client('IMF_DATA')
    try:
        msg = client.data(
            resource_id=resource_id,
            key=key,
            params=params or {},
            headers=headers
        )
        temp = sdmx.to_pandas(msg)
        df = temp.reset_index()
        df.head()
        if convert_dates:
            df = convert_time_period_auto(df, time_col='TIME_PERIOD', out_col='date')  # ✅ now returns df

        return df

    except Exception as e:
        raise RuntimeError(f"Error fetching {resource_id}: {e}")