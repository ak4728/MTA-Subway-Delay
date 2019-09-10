# MTA Subway Delays
This is a repository for collecting real-time data from the MTA Developer API to compute subway delays at each station.

## Requirements
- MTA SUBWAY API KEY: [Click here to register and get a MTA API KEY](https://datamine.mta.info/user/register)
- python libraries: os, time, datetime, requests, pandas, gtfs-realtime-bindings.  
Please run codes below in terminal to prepare the dependent libraries:  
``` python
pip install --upgrade requests, datetime, pandas, gtfs-realtime-bindings
```

## Installation
``` python
pip install git+https://github.com/ak4728/MTA-Subway-Delay.git
```

## Usage
### Terminal
#### Execution
Please run codes below in terminal and then input your MTA SUBWAY API KEY:
```python
python MTAGTFS.py
```

#### Exit
To stop your program, please press ```Control + C```.

### Jupyter Notebook
``` python
import MTAGTFS
```
``` python
# 'collect' function takes APIkey as an input, keeps requesting MTA subway real-time status and Writting gtfs files.
# Output GTFS files to the corresponding folder: e.g. ~/201808/20180801/gtfs_1_2018-08-01-12-00-00.gtfs
APIkey = 'YOUR MTA SUBWAY API KEY'
MTAGTFS.collect(APIkey)
```
``` python
# 'arrival' function takes date as an input, structures and integrates the GTFS files, and outputs a arrival csv file.
# Require GTFS files prepared in the corresponding folder: e.g. ~/201808/20180801/gtfs_ace_20180801_041946.gtfs
# Output actual arrival csv file to the corresponding folder: e.g. ~/201808/arrival_20180801.csv
date = '20180801'
MTAGTFS.arrival(date)
```

``` python
# 'delay' takes date as an input, calculates delays by actual arrivals and schedules, and outputs a delay csv file.
# Require actual arrival csv file prepared in the corresponding folder: e.g. ~/201808/arrival_20180801.csv
# Output calculated delay csv file to the corresponding folder: e.g. ~/201808/delay_20180801.csv
date = '20180801'
MTAGTFS.delay(date)
```
## Update Interval
15 seconds per update on average

## Data Source
### Schedules
GTFS schedule data is refreshed whenever warranted by service changes, on average about every 4 months
- [Most Recent GTFS Schedules from MTA](http://web.mta.info/developers/data/nyct/subway/google_transit.zip)
- [Most Recent PDF Schedules from MTA](https://new.mta.info/schedules)
- [Historical GTFS Schedules from OpenMobilityData](https://transitfeeds.com/p/mta/79)

### Actual Arrivals
#### Real-time
- [MTA API](http://datamine.mta.info/list-of-feeds)
- [MTA APP](http://subwaytime.mta.info/)
- [MTA Portal](https://new.mta.info/)
- [OpenMobilityData](https://transitfeeds.com/p/mta/234)

#### Historical
- [MTA Data Feeds](http://web.mta.info/developers/developer-data-terms.html#data)
- [B-Division (Letter trains)](http://web.mta.info/developers/data/archives.html)
- [A-Division (Numeric trains)](https://datamine-history.s3.amazonaws.com/index.html)
## Reference
### Web Application
- [subwaystats](http://subwaystats.com/)
- [MTA dashboard](http://dashboard.mta.info/)

### MTA GTFS Dictionary
- [GTFS-realtime Reference](http://datamine.mta.info/sites/all/files/pdfs/GTFS-Realtime-NYC-Subway%20version%201%20dated%207%20Sep.pdf)

## Bias & Limitation
- Sampling process
  - Not all arrival data is uploaded in this MTA real-time system.
  - Abnormal data exists (abnormal time/ trip_id), and they were filtered.
  - Sampling rate reported.
