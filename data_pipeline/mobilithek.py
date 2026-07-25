import pandas as pd
from abc import ABC, abstractmethod

class Mobilithek(ABC):
    @abstractmethod
    def get_data(self):
        pass

class MobilithekRemote(Mobilithek):
    def __init__(self, url) -> None:
        self.url = url
        self.df = None
    
    def get_data(self):
        if self.url:
            self.df = pd.read_csv(self.url, delimiter=";", encoding='latin-1')
            return self.df
    
    def save_data_to_local_storage(self, path):
        if self.df is None:
            self.get_data()
        
        self.df.to_csv(path, sep=";")
            
    
class MobilithekLocal(Mobilithek):
    def __init__(self, path) -> None:
        self.path = path
    
    def get_data(self):
        return pd.read_csv(self.path, delimiter=";")