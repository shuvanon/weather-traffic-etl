from data_pipeline.pipeline import Pipeline
from data_pipeline.extract import Extractor
from data_pipeline.transform import Transformer
from data_pipeline.load import Loader
import os

def test_db_not_exists():
    path = "data/data.sqlite"
    if os.path.exists(path):
        os.remove(path)
    assert os.path.exists(path) == False
    
    
def test_run_pipeline():
    extractor = Extractor()
    transformer = Transformer()
    loader = Loader('weather_traffic_fines','data/data.sqlite')
    pipeline = Pipeline(extractor, transformer, loader)
    pipeline.run()
    assert os.path.exists("./data/data.sqlite")