from data_pipeline.extract import Extractor
from data_pipeline.power_api import PowerAPILocal
from data_pipeline.mobilithek import MobilithekLocal


def test_extractor_uses_injected_sources_offline(fixtures_dir):
    extractor = Extractor(
        weather_source=PowerAPILocal(str(fixtures_dir / "weather_sample.csv")),
        traffic_source=MobilithekLocal(str(fixtures_dir / "traffic_sample.csv")),
    )

    weather = extractor.get_weather_data()
    traffic = extractor.get_traffic_data()

    assert "T2M" in weather.columns
    assert weather.shape[0] == 3
    assert "TATTAG" in traffic.columns
    assert traffic.shape[0] == 6


class _RecordingSource:
    """Minimal source that records that get_data() was called."""

    def __init__(self, frame):
        self.frame = frame
        self.called = False

    def get_data(self):
        self.called = True
        return self.frame


def test_extractor_delegates_to_the_injected_source():
    import pandas as pd

    sentinel = pd.DataFrame({"T2M": [1.0]}, index=["20220101"])
    source = _RecordingSource(sentinel)
    extractor = Extractor(weather_source=source)

    result = extractor.get_weather_data()

    assert source.called is True
    assert result is sentinel
