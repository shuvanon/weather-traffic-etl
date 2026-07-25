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
    def get_weather_data(self):
        conf = self.get_config()
        return PowerAPIRemote(
            base_url=conf["power_api_base_url"],
            start=pd.Timestamp(str(conf["start_date"])),
            end=pd.Timestamp(str(conf["end_date"])),
            long=conf["lon"],
            lat=conf["lat"],
            parameter=conf["parameter"],
        ).get_data()

    def save_weather_data(self):
        output_path = self.get_output_path(self.get_config(), "weather_data.csv")
        self.get_weather_data().to_csv(output_path, sep=";")

    def get_traffic_data(self):
        conf = self.get_config()
        return MobilithekRemote(conf["traffic_data_base_url"]).get_data()

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
