from data_pipeline.pipeline import Pipeline
from data_pipeline.extract import Extractor
from data_pipeline.transform import Transformer
from data_pipeline.load import Loader
from data_pipeline.power_api import PowerAPILocal
from data_pipeline.mobilithek import MobilithekLocal


def test_pipeline_end_to_end_offline(tmp_path, fixtures_dir):
    db_path = tmp_path / "analysis.sqlite"
    extractor = Extractor(
        weather_source=PowerAPILocal(str(fixtures_dir / "weather_sample.csv")),
        traffic_source=MobilithekLocal(str(fixtures_dir / "traffic_sample.csv")),
    )
    loader = Loader("weather_traffic_fines", str(db_path))

    Pipeline(extractor, Transformer(), loader).run()

    assert db_path.exists()

    result = loader.read_data_from_sqlite()
    # Weather (Jan 1-3) merged with traffic on overlapping dates -> 3 rows.
    assert result.shape[0] == 3
    assert "TRAFFIC OFFENCE FREQUENCIES" in result.columns
    assert sorted(result["TRAFFIC OFFENCE FREQUENCIES"].tolist()) == [1, 2, 3]
