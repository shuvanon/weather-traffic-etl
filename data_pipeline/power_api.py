from typing import List, Union, Optional
from pathlib import Path
from datetime import date, datetime
import requests
import pandas as pd
from abc import ABC, abstractmethod

class PowerAPI(ABC):
    @abstractmethod
    def get_data(self):
        pass

class PowerAPIRemote(PowerAPI):
    def __init__(self,
                 base_url: str,
                 start: Union[date, datetime, pd.Timestamp],
                 end: Union[date, datetime, pd.Timestamp],
                 long: float, lat: float,
                 use_long_names: bool = False,
                 parameter: Optional[List[str]] = None):
        self.base_url = base_url
        self.start = start
        self.end = end
        self.long = long
        self.lat = lat
        self.use_long_names = use_long_names
        self.parameter = parameter

        self.request = self._build_request()

    def _build_request(self):
        r = self.base_url
        r += f"parameters={(',').join(self.parameter)}"
        r += '&community=RE'
        r += f"&longitude={self.long}"
        r += f"&latitude={self.lat}"
        r += f"&start={self.start.strftime('%Y%m%d')}"
        r += f"&end={self.end.strftime('%Y%m%d')}"
        r += '&format=JSON'

        return r

    def get_data(self):
        response = requests.get(self.request, timeout=30)
        response.raise_for_status()

        records = response.json()['properties']['parameter']
        return pd.DataFrame.from_dict(records)
    
    def save_data_to_local_storage(self, path):
        if self.df is None:
            self.get_data()
        
        self.df.to_csv(path, sep=";")
        
class PowerAPILocal(PowerAPI):
    def __init__(self, path) -> None:
        self.path = path

    def get_data(self):
        # Mirror PowerAPIRemote.get_data(): a date-indexed frame with one
        # column per parameter (the first CSV column holds the dates).
        return pd.read_csv(self.path, delimiter=";", index_col=0)