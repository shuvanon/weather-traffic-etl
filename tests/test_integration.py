"""Live integration tests that hit the real NASA POWER and Bonn Open Data
endpoints. Deselected by default (see pytest.ini); run explicitly with:

    pytest -m integration
"""
import pytest

from data_pipeline.extract import Extractor
from data_pipeline.transform import Transformer
from data_pipeline.load import Loader
from data_pipeline.pipeline import Pipeline

pytestmark = pytest.mark.integration


def test_live_weather_extract_has_expected_columns():
    df = Extractor().get_weather_data()
    assert not df.empty
    for column in ("T2M", "PRECTOTCORR", "WS10M"):
        assert column in df.columns


def test_live_traffic_extract_has_date_column():
    df = Extractor().get_traffic_data()
    assert not df.empty
    assert "TATTAG" in df.columns


def test_live_pipeline_writes_sqlite(tmp_path):
    db_path = tmp_path / "analysis.sqlite"
    loader = Loader("weather_traffic_fines", str(db_path))

    Pipeline(Extractor(), Transformer(), loader).run()

    assert db_path.exists()
    assert loader.read_data_from_sqlite().shape[0] > 0
