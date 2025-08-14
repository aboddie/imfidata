from __future__ import annotations
import sdmx

# Single place to construct the SDMX client in case you want to customize later.
def get_client() -> sdmx.Client:
    # 'IMF_DATA' is the IMF SDMX endpoint configured in pandasdmx

    return sdmx.Client("IMF_DATA")
