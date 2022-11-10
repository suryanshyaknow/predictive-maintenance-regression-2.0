# About Project

**Project Description**

Predictive maintenance algorithms use data including: all necessary maintenance, remaining useful life (RUL), historical data, maintenance records, operating conditions, failure patterns, regression models, and much more. It goes without saying that real predictive maintenance datasets are generally difficult to obtain and in particular difficult to publish, so here I did analysis on the synthetiuc dataset that reflects real predictive maintenance encountered in industry to the best of the knowledge. Here, I however tried to regress against the Air Temperature to predict its value with highest accuracy possible, provided all other relevant attributes at hand are known to us -- **Air temperature**, **Rotational speed**, **Torque**, **Tool wear** and the **Machine failures** which further are categorized into five independent faiures viz. **TWF (Tool Wear Failure)**, **HDF (Heat Dissipation Failure)**, **PWF (Power Failure)**, **OSF (Overstarin Failure)** and **RNF (Random failure)**.
<br>Moreover, the project's pipeline is automated to the scratch via DVC.

## About Dataset

### Attribute Information:

The dataset consists of 10,000 data points stored as rows with 14 features in columns.
- **UID**: unique identifier ranging from 1 to 10000
- **product ID**: consisting of a letter L, M, or H for low (50% of all products), medium (30%) and high (20%) as product quality - variants and a variant-specific serial number
- **air temperature [K]**: generated using a random walk process later normalized to a standard deviation of 2 K around 300 K
- **process temperature [K]**: generated using a random walk process normalized to a standard deviation of 1 K, added to the air - temperature plus 10 K.
- **rotational speed [rpm]**: calculated from a power of 2860 W, overlaid with a normally distributed noise
- **torque [Nm]**: torque values are normally distributed around 40 Nm with a Ïƒ = 10 Nm and no negative values.
- **tool wear [min]**: The quality variants H/M/L add 5/3/2 minutes of tool wear to the used tool in the process. and a 'machine failure' label that indicates, whether the machine has failed in this particular datapoint for any of the following failure modes are true.

### The Machine failure consists of five independent failure modes: 

- **tool wear failure (TWF)**: the tool will be replaced of fail at a randomly selected tool wear time between 200 and 240 mins (120 times in our dataset). At this point in time, the tool is replaced 69 times, and fails 51 times (randomly assigned).
- **heat dissipation failure (HDF)**: heat dissipation causes a process failure, if the difference between air- and process temperature is below 8.6 K and the tool's rotational speed is below 1380 rpm. This is the case for 115 data points.
- **power failure (PWF)**: the product of torque and rotational speed (in rad/s) equals the power required for the process. If this power is below 3500 W or above 9000 W, the process fails, which is the case 95 times in our dataset.
- **overstrain failure (OSF)**: if the product of tool wear and torque exceeds 11,000 minNm for the L product variant (12,000 M, 13,000 H), the process fails due to overstrain. This is true for 98 datapoints.
- **random failures (RNF)**: each process has a chance of 0.1% to fail regardless of its process parameters. This is the case for only 5 datapoints, less than could be expected for 10,000 datapoints in our dataset.

**Note:** If at least one of the above failure modes is true, the process fails and the `machine failure` is set to 1. It is therefore not transparent to the machine learning method, which of the failure modes has caused the process to fail.

### Dataset's Description:


```python
predictive_maintenance.info()
```

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 9541 entries, 0 to 9540
    Data columns (total 11 columns):
     #   Column                   Non-Null Count  Dtype  
    ---  ------                   --------------  -----  
     0   Air temperature [K]      9541 non-null   float64
     1   Process temperature [K]  9541 non-null   float64
     2   Rotational speed [rpm]   9541 non-null   float64
     3   Torque [Nm]              9541 non-null   float64
     4   Tool wear [min]          9541 non-null   float64
     5   Machine failure          9541 non-null   int64  
     6   TWF                      9541 non-null   int64  
     7   HDF                      9541 non-null   int64  
     8   PWF                      9541 non-null   int64  
     9   OSF                      9541 non-null   int64  
     10  RNF                      9541 non-null   int64  
    dtypes: float64(5), int64(6)
    memory usage: 820.1 KB
    


```python
predictive_maintenance.describe()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Air temperature [K]</th>
      <th>Process temperature [K]</th>
      <th>Rotational speed [rpm]</th>
      <th>Torque [Nm]</th>
      <th>Tool wear [min]</th>
      <th>Machine failure</th>
      <th>TWF</th>
      <th>HDF</th>
      <th>PWF</th>
      <th>OSF</th>
      <th>RNF</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>9541.000000</td>
      <td>9541.000000</td>
      <td>9541.000000</td>
      <td>9541.000000</td>
      <td>9541.000000</td>
      <td>9541.000000</td>
      <td>9541.000000</td>
      <td>9541.000000</td>
      <td>9541.000000</td>
      <td>9541.000000</td>
      <td>9541.000000</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>299.993921</td>
      <td>310.000314</td>
      <td>1515.186878</td>
      <td>40.783220</td>
      <td>108.017923</td>
      <td>0.027984</td>
      <td>0.004402</td>
      <td>0.011739</td>
      <td>0.003144</td>
      <td>0.009328</td>
      <td>0.001991</td>
    </tr>
    <tr>
      <th>std</th>
      <td>1.995795</td>
      <td>1.481177</td>
      <td>129.878502</td>
      <td>8.921248</td>
      <td>63.580291</td>
      <td>0.164937</td>
      <td>0.066205</td>
      <td>0.107714</td>
      <td>0.055989</td>
      <td>0.096136</td>
      <td>0.044583</td>
    </tr>
    <tr>
      <th>min</th>
      <td>295.300000</td>
      <td>305.700000</td>
      <td>1168.000000</td>
      <td>20.100000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>298.300000</td>
      <td>308.800000</td>
      <td>1420.000000</td>
      <td>34.200000</td>
      <td>53.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>300.100000</td>
      <td>310.100000</td>
      <td>1496.000000</td>
      <td>40.600000</td>
      <td>108.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>301.500000</td>
      <td>311.100000</td>
      <td>1595.000000</td>
      <td>47.000000</td>
      <td>162.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>max</th>
      <td>304.500000</td>
      <td>313.800000</td>
      <td>1895.000000</td>
      <td>67.000000</td>
      <td>253.000000</td>
      <td>1.000000</td>
      <td>1.000000</td>
      <td>1.000000</td>
      <td>1.000000</td>
      <td>1.000000</td>
      <td>1.000000</td>
    </tr>
  </tbody>
</table>
</div>



## Project Snapshot
<div>
<center> <img src="project_snapshot.png"> </center>
</div>