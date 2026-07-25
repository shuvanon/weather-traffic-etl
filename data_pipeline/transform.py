import pandas as pd


class Transformer:
    def transform_weather_data(self, df=pd.DataFrame):
        # Move the date index into a column and parse it as a datetime.
        df = df.reset_index(names="DATE")
        df["DATE"] = pd.to_datetime(df["DATE"], format="%Y%m%d")
        return df

    def transform_traffic_data(self, df=pd.DataFrame):
        # Parse dates and count the number of offences recorded on each day.
        df["TATTAG"] = pd.to_datetime(df["TATTAG"], format="%d.%m.%Y")
        date_counts = df.groupby("TATTAG")["TATTAG"].count()
        return pd.DataFrame(
            {"DATE": date_counts.index, "TRAFFIC OFFENCE FREQUENCIES": date_counts.values}
        )

    def merge_datasets(self, weather=pd.DataFrame, traffic=pd.DataFrame):
        df = pd.merge(weather, traffic, on="DATE")
        return df.set_index(df.columns[0], drop=True)
