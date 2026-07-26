from pathlib import Path

import pandas as pd
import yaml

from data_pipeline.power_api import PowerAPIRemote
from data_pipeline.mobilithek import MobilithekRemote

# Resolve paths relative to this file so the pipeline runs from any working directory.
_MODULE_DIR = Path(__file__).resolve().parent      # .../data_pipeline
_PROJECT_ROOT = _MODULE_DIR.parent                 # repository root
_CONFIG_FILE = _MODULE_DIR / "config.yaml"


class Extractor:
    """Fetches the weather and traffic datasets.

    By default the data is pulled from the live remote sources built from
    ``config.yaml``. Tests (or offline runs) can inject alternative sources
    that satisfy the same ``get_data()`` interface, e.g. ``PowerAPILocal`` /
    ``MobilithekLocal`` reading from fixture files.
    """

    def __init__(self, weather_source=None, traffic_source=None):
        self._weather_source = weather_source
        self._traffic_source = traffic_source

    def get_weather_data(self):
        source = self._weather_source or self._remote_weather_source()
        return source.get_data()

    def get_traffic_data(self):
        source = self._traffic_source or self._remote_traffic_source()
        return source.get_data()

    def _remote_weather_source(self):
        conf = self.get_config()
        return PowerAPIRemote(
            base_url=conf["power_api_base_url"],
            start=pd.Timestamp(str(conf["start_date"])),
            end=pd.Timestamp(str(conf["end_date"])),
            long=conf["lon"],
            lat=conf["lat"],
            parameter=conf["parameter"],
        )

    def _remote_traffic_source(self):
        conf = self.get_config()
        return MobilithekRemote(conf["traffic_data_base_url"])

    def save_weather_data(self):
        output_path = self.get_output_path(self.get_config(), "weather_data.csv")
        self.get_weather_data().to_csv(output_path, sep=";")

    def save_traffic_data(self):
        output_path = self.get_output_path(self.get_config(), "traffic_data.csv")
        self.get_traffic_data().to_csv(output_path, sep=";")

    def get_config(self):
        with open(_CONFIG_FILE, "rb") as f:
            return yaml.load(f, Loader=yaml.FullLoader)

    def get_output_path(self, conf, filename: str):
        output_dir = _PROJECT_ROOT / conf.get("output_dir", "data")
        output_dir.mkdir(parents=True, exist_ok=True)
        return output_dir / filename
