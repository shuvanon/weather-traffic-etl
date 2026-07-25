from data_pipeline.load import Loader
import pandas as pd
#T2M;T2MDEW;QV2M;PRECTOTCORR;PS;WS10M;WD10M
def test_if_data_loaded_to_SQLite():
    data = {
        'T2M': [2.5, 3.0, 2.0, 1.5],
        'T2MDEW': [8.08,0.01,-.52, 2.96],
        'QV2M': [6,3,5,9],
        'PRECTOTCORR': [4.6, 5.2, 3.4, 4.5],
        'PS': [99,98,96,98],
        'WS10M': [3.6, 4.2, 5.1, 2.8],
        'WD10M': [218,250,310,285]
        }
    load_df = pd.DataFrame(data)
    loader = Loader('weather_traffic_fines','data/data.sqlite')
    loader.load_data_to_sqlite(load_df)
    
    read_df = loader.read_data_from_sqlite()
    read_df = read_df.set_index(read_df.columns[0], drop=True)

    assert load_df.shape == read_df.shape