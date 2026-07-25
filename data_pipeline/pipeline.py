import logging
from pathlib import Path

from data_pipeline.extract import Extractor
from data_pipeline.transform import Transformer
from data_pipeline.load import Loader

logger = logging.getLogger(__name__)


class Pipeline:
    def __init__(self, extractor, transformer, loader) -> None:
        self.__extractor = extractor
        self.__transformer = transformer
        self.__loader = loader

    def run(self):
        logger.info("Extracting weather data")
        weather_data = self.__extractor.get_weather_data()

        logger.info("Extracting traffic data")
        traffic_data = self.__extractor.get_traffic_data()

        logger.info("Transforming datasets")
        transform_weather_data = self.__transformer.transform_weather_data(weather_data)
        transform_traffic_data = self.__transformer.transform_traffic_data(traffic_data)

        logger.info("Merging datasets")
        merge_data = self.__transformer.merge_datasets(transform_weather_data, transform_traffic_data)

        logger.info("Loading merged data into SQLite")
        self.__loader.load_data_to_sqlite(merge_data)
        logger.info("Pipeline finished")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    db_path = Path(__file__).resolve().parent.parent / "data" / "data.sqlite"
    extractor = Extractor()
    transformer = Transformer()
    loader = Loader("weather_traffic_fines", str(db_path))
    Pipeline(extractor, transformer, loader).run()
