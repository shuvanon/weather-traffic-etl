from data_pipeline.transform import Transformer
from data_pipeline.extract import Extractor
from datetime import datetime
import pytest

@pytest.fixture
def transformer():
    return Transformer()

@pytest.fixture
def extractor():
    return Extractor()

def test_weather_data_after_transformation(transformer, extractor):
    weather_data = extractor.get_weather_data()
    transformed_data = transformer.transform_weather_data(weather_data)
    assert weather_data.shape[0] == transformed_data.shape[0]
    assert weather_data.shape[1] == transformed_data.shape[1] - 1
    assert isinstance(transformed_data["DATE"][0], datetime) is True 

def test_traffic_data_after_transformation(transformer, extractor):
    traffic_data = extractor.get_traffic_data()
    transformed_data = transformer.transform_traffic_data(traffic_data)
    assert transformed_data.shape[1] == 2
    assert transformed_data.columns[0] == "DATE" and transformed_data.columns[1] == "TRAFFIC OFFENCE FREQUENCIES"