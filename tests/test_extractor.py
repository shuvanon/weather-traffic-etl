from data_pipeline.extract import Extractor
import os
import pytest

@pytest.fixture
def extractor():
    return Extractor()

def test_if_weather_data_is_extracted(extractor):
    extractor.save_weather_data()
    
    assert os.path.exists("./data/weather_data.csv")
    
def test_if_traffic_data_is_extracted(extractor):
    extractor.save_traffic_data()
    
    assert os.path.exists("./data/traffic_data.csv")