# Project Plan

## Title
Exploring the Relationship Between Weather Conditions and Traffic Offences in Bonn (2022)


## Main Question

<!-- Think about one main question you want to answer based on the data. -->
1. How does temperature affect the occurrence of speeding?
2. Is there a correlation between wind conditions and instances of exceeding the speed limit?
3. Does precipitation have any impact on the likelihood of traffic fines due to speeding in the Bonn city area?
4. Are there any patterns or trends in the data that suggest a consistent relationship between weather variables (temperature, wind, precipitation) and traffic violations related to speeding?

## Description

<!-- Describe your data science project in max. 200 words. Consider writing about why and how you attempt it. -->

This study investigates the correlation between weather conditions and speeding offences within the Bonn city area. It examines instances of traffic fines resulting from exceeding speed limits, exploring their relationship with temperature, wind, and precipitation on specific dates throughout the year 2022, spanning from January to December.


## Datasources

<!-- Describe each datasources you plan to use in a section. Use the prefic "DatasourceX" where X is the id of the datasource. -->

### Datasource1: Bußgelder fließender Verkehr 2022
* Metadata URL: https://mobilithek.info/offers/-5415240082314561823
* Data URL: https://opendata.bonn.de/sites/default/files/Geschwindigkeitsverstoesse2022.csv
* Data Type: CSV


### Datasource2: NASA Prediction Of Worldwide Energy Resources
* Metadata URL: https://power.larc.nasa.gov/data-access-viewer
* Data URL: https://power.larc.nasa.gov/api/temporal/daily/point
* Data Type: JSON (NASA POWER API)

This weather dataset is generated from the POWER project using the following options:
* Date: Jan 01, 2022 to Dec 31, 2022
* Temporal: Daily
* Location: Bonn
* Parameters: Temperature at 2 Meters, Precipitation, Wind Speed at 10 Meters.


## Work Packages

1. Acquire the two data sources — NASA POWER daily weather and the Bonn "speeding fines 2022" open dataset.
2. Build an ETL pipeline that extracts, cleans, merges the datasets on date, and loads them into a SQLite database.
3. Explore the data — distributions and seasonal trends — in `exploration.ipynb`.
4. Analyse the correlation between weather parameters and traffic-offence frequencies, and write up the findings in `report.ipynb`.
5. Add automated tests and continuous integration for the pipeline.
