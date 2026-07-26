import pandas as pd

from data_pipeline import power_api
from data_pipeline.power_api import PowerAPIRemote, PowerAPILocal


def _remote():
    return PowerAPIRemote(
        base_url="https://example.test/api?",
        start=pd.Timestamp("2022-01-01"),
        end=pd.Timestamp("2022-12-31"),
        long=7.1019,
        lat=50.7324,
        parameter=["T2M", "WS10M"],
    )


def test_build_request_contains_all_query_parameters():
    req = _remote().request
    assert req.startswith("https://example.test/api?")
    assert "parameters=T2M,WS10M" in req
    assert "longitude=7.1019" in req
    assert "latitude=50.7324" in req
    assert "start=20220101" in req
    assert "end=20221231" in req
    assert "format=JSON" in req


class _FakeResponse:
    def __init__(self, payload):
        self._payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self._payload


def test_get_data_parses_api_json(monkeypatch):
    payload = {
        "properties": {
            "parameter": {
                "T2M": {"20220101": 5.0, "20220102": 6.0},
                "WS10M": {"20220101": 3.0, "20220102": 2.5},
            }
        }
    }
    monkeypatch.setattr(power_api.requests, "get", lambda url, timeout=None: _FakeResponse(payload))

    df = _remote().get_data()

    assert list(df.columns) == ["T2M", "WS10M"]
    assert df.shape == (2, 2)
    assert df.loc["20220101", "T2M"] == 5.0


def test_power_api_local_reads_fixture_as_date_indexed_frame(fixtures_dir):
    df = PowerAPILocal(str(fixtures_dir / "weather_sample.csv")).get_data()

    assert list(df.columns) == ["T2M", "T2MDEW", "QV2M", "PRECTOTCORR", "PS", "WS10M", "WD10M"]
    assert df.shape[0] == 3
