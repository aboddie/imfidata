from __future__ import annotations
import re
from dataclasses import dataclass, field
from typing import Dict, Iterable, List
import pandas as pd


def sanitize(name: str) -> str:
    """Convert any string into a valid Python identifier."""
    if not isinstance(name, str):
        name = str(name)
    name = re.sub(r"[^a-zA-Z0-9\s]", "_", name)
    name = re.sub(r"\s+", "_", name)
    name = re.sub(r"_+", "_", name)
    name = name.strip("_")
    if not name or not name[0].isalpha():
        name = "X" + name
    return name


@dataclass
class DimensionEnv:
    """
    Simple dot-accessible container for code lists.
    """
    _attrs: Dict[str, str] = field(default_factory=dict)

    def __getattr__(self, item: str) -> str:
        try:
            return self._attrs[item]
        except KeyError as e:
            raise AttributeError(item) from e

    def __dir__(self) -> List[str]:
        return sorted(list(self._attrs.keys()))

    def __repr__(self) -> str:
        pairs = ", ".join(f"{k}={v!r}" for k, v in self._attrs.items())
        return f"DimensionEnv({pairs})"

def make_env_from_pairs(pairs: Iterable[tuple[str, str]]) -> DimensionEnv:
    attrs: Dict[str, str] = {}
    for label, code in pairs:
        key = sanitize(label)
        if key not in attrs:
            attrs[key] = code
        # silently skip duplicates
    return DimensionEnv(attrs)

def make_env_from_df(df, col1: str, col2:str) -> DimensionEnv:
    pairs: Iterable[tuple[str, str]] = [(row[col1], row[col2]) for _, row in df.iterrows()]
    return make_env_from_pairs(pairs)


def old_make_key_str(key: List[List[str]]) -> str:
    """
    Convert list-of-lists to SDMX key string.
    Example: [["USA","CAN"], ["LUR"], ["A"]] -> "USA+CAN.LUR.A"
    """
    return ".".join("+".join(inner) if inner else "" for inner in key)


def make_key_str(key) -> str:
    parts = []
    for group in key:
        if group is None or (isinstance(group, list) and len(group) == 0):
            part = ""
        elif isinstance(group, str):
            part = str(group)  # single string
        else:
            # Assume it's an iterable (list, tuple, R vector, etc.)
            items = [str(x) for x in group if x is not None and x != "" and not str(x).lower() == "null"]
            part = "+".join(items) if items else ""
        parts.append(part)
    return ".".join(parts)

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
