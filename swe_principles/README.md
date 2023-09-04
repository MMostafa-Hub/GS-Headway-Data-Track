# Time Series Simulator

 is a simple and easy-to-use tool for generating time series data samples. It uses pandas and numpy to generate the samples. And it uses matplotlib for visualizing the data.

## Features

-   Can specify the attributes through a configuration file, e.g. `config.yaml` file.
-   Save the data in various formats, e.g. `timeseries.csv` file.
-   Visualize the generated sample.
-   The ability to extend the program, by adding your custom functions or classes. (see the class diagram)
#Seenstallation

To use Time Series Simulator, you will need Python 3 and the following dependencies:

-   Pandas
-   Matplotlib
-   Numpy
-   Pyyaml

You can install these using pip:
```
pip install pandas matplotlib numpy pyyaml
```

## Usage

1.  Input desired configurations in the `config.yaml` file.
2.  Open a terminal in the project directory and run `timesereis_client.py`

## Example
1. Modify `config.yaml` for the desired time series sample
```yaml
# Time index parameters
# 1 Year of timeseries data with 1 minute sampling frequency
time_index: {
  start_date: "2019-01-01",
  end_date: "2023-01-01",
  sampling_frequency_in_minutes: 60 # 1 hour
}

# Main components parameters
multiplicative: True,
main_components: {
  trend: {
    coefficients: [0.005, 0.001] ,
  },
  # You can add more than one seasonality component
  seasonality: [
    {
      in_days: False,
      period: 24, # Daily
      amplitude: 0.5
    },
    {
      in_days: True,
      period: 365, # Yearly
      amplitude: 0.005
    }
  ] ,
}

# Residual components parameters
residual_components: {
  noise: {
    noise_level: 0.1
  },
  outliers: {
    outlier_ratio: 0.001
  },
}
```
2. run `timeseries_client.py` in terminal
```bash
python timeseries_client.py
```
3. Check the resulting visualization.
<p align="center">
    <img src="https://github.com/MMostafa-Hub/Headway-GS-Data-Track-Tasks/blob/main/images/vis.JPG">
</p>
  4. Once you're happy with the result you could just use the generated data sample in your next app.

## Extensibility 
- Check the UML class diagram in `timesereis_simulator.drawio`.
- You can add a new `Transformer` or a `Generator` by just inheriting from the abstract classes
- You can add a new type of data dump or configuration by just adding a new function with the new type.
  ```python
  ConfigurationManager.env(path: str) -> TimeSeriesParams:
   ...
  ```
  ```python
  TimeSeriesProducer.tsv(path: str) -> None:
   ...
  ```
