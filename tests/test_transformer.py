from datetime import datetime

import pandas as pd

from data_pipeline.transform import Transformer

WEATHER_PARAMS = ["T2M", "T2MDEW", "QV2M", "PRECTOTCORR", "PS", "WS10M", "WD10M"]


def _weather_frame():
    """A frame shaped like PowerAPIRemote.get_data(): date-string index, one column per parameter."""
    index = ["20220101", "20220102", "20220103"]
    data = {p: [1.0, 2.0, 3.0] for p in WEATHER_PARAMS}
    return pd.DataFrame(data, index=index)


def test_transform_weather_data_adds_a_datetime_date_column():
    raw = _weather_frame()
    out = Transformer().transform_weather_data(raw)

    assert out.columns[0] == "DATE"
    assert out.shape[0] == raw.shape[0]          # same number of rows
    assert out.shape[1] == raw.shape[1] + 1      # gains the DATE column
    assert isinstance(out["DATE"].iloc[0], datetime)
    assert out["DATE"].iloc[0] == pd.Timestamp("2022-01-01")


def test_transform_traffic_data_counts_offences_per_day():
    raw = pd.DataFrame({"TATTAG": ["01.01.2022", "01.01.2022", "02.01.2022"], "PLACE": ["a", "b", "c"]})
    out = Transformer().transform_traffic_data(raw)

    assert list(out.columns) == ["DATE", "TRAFFIC OFFENCE FREQUENCIES"]
    assert out["TRAFFIC OFFENCE FREQUENCIES"].tolist() == [2, 1]
    assert out["DATE"].tolist() == [pd.Timestamp("2022-01-01"), pd.Timestamp("2022-01-02")]


def test_merge_datasets_joins_on_overlapping_dates():
    weather = Transformer().transform_weather_data(_weather_frame())
    traffic = pd.DataFrame(
        {
            "DATE": pd.to_datetime(["2022-01-01", "2022-01-03"]),
            "TRAFFIC OFFENCE FREQUENCIES": [5, 9],
        }
    )
    merged = Transformer().merge_datasets(weather, traffic)

    assert merged.index.name == "DATE"
    assert merged.shape[0] == 2                  # only the two overlapping dates survive
    assert "TRAFFIC OFFENCE FREQUENCIES" in merged.columns
    assert merged["TRAFFIC OFFENCE FREQUENCIES"].tolist() == [5, 9]
