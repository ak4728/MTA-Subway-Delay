# MTA Subway Delays
This is a repository for collecting real-time data from the MTA Developer API to compute subway delays at each station.

## Requirements
- MTA SUBWAY API KEY: [Click here to register an MTA API KEY](https://datamine.mta.info/user/register)
- Dependent python libraries: os, time, datetime, requests, pandas, gtfs-realtime-bindings.  
Please run codes below in terminal to prepare dependent libraries:  
``` python
pip install --upgrade requests, datetime, pandas, gtfs-realtime-bindings
```

## Installation
Please run codes below in terminal to install mtagtfs.  
Administrator permission is required.
``` python
pip install --upgrade git+https://github.com/ak4728/MTA-Subway-Delay.git
```

## Usage
### Terminal
#### collect function
Take APIkey as an input, keep requesting MTA subway real-time status and writting gtfs files;  
Require mtagtfs.py in the current working directory;  
To stop this program, please press ```Control + C```.
```python
python mtagtfs.py
```

### Jupyter Notebook
``` python
import mtagtfs
```
#### collect function
Take APIkey as an input, keep requesting MTA subway real-time status and writting gtfs files;  
Output GTFS files to the corresponding folder: e.g. ~/201808/20180801/gtfs_1_2018-08-01-12-00-00.gtfs.
``` python
APIkey = 'YOUR MTA SUBWAY API KEY'
mtagtfs.collect(APIkey)
```
#### arrival function
Take date as an input, structure and integrate the GTFS files, and output an arrival csv file;  
Require GTFS files prepared in the corresponding folder: e.g. ~/201808/20180801/gtfs_ace_20180801_041946.gtfs;  
Output actual arrival csv file to the corresponding folder: e.g. ~/201808/arrival_20180801.csv.  
``` python
date = '20180801'
mtagtfs.arrival(date)
```

#### delay function
Take date as an input, calculate delays by actual arrivals and schedules, and output a delay csv file;  
Require actual arrival csv file prepared in the corresponding folder: e.g. ~/201808/arrival_20180801.csv;  
Output calculated delay csv file to the corresponding folder: e.g. ~/201808/delay_20180801.csv.  
``` python
# Default schedule date is the latest one
date = '20190901'
mtagtfs.delay(date)

# For historical schedules, please set the argument date_schedule; refer to: https://transitfeeds.com/p/mta/79.
date = '20180801'
mtagtfs.delay(date, date_schedule = '20180708') # '20180708' is the schedule releasing date
```
## Application
- Visualization Website: [MTA SUBWAY DELAY](https://public.tableau.com/profile/junjie.cai#!/vizhome/Book1_15686658217570/MTASUBWAYDELAY)

## Data Description
### Update Interval
- Real-time status updates per 15 seconds on average;
- Schedules update every 4 months on average.

### Historical Data Availability
| MTA Division | Start Date |	End Date	| Notes |
| ------------- |:-------------:| :-------------:| :-------------:|
|A-division (Numeric trains)|2014-09-16|2018-10-13|Daily packaged tgz file from AWS |
|B-division  (Letter trains)|2018-08-01|2019-06-01|Monthly packaged zip file from MTA|


### Column Explanation
| Column Name | Explanation |
| ------------- |:-------------:|
|**'arrival_time'**|actual arrival time|
|**'arrival_time_scheduled'**|scheduled arrival time|
|'departure_time_scheduled'|scheduled departure time|
|**'delay'**|calculated delay in seconds|
|**'stop_id'**|arrival stop id|
|**'route_id'**|route id|
|'gtfs_timestamp'|status report time|
|'trip_id'|trip id|
|'current_stop_sequence'|arrival stop sequence when reporting status|
|'current_status'|stop status when reporting status (1|STOPPED_AT| 2||IN_TRANSIT_TO)|
|'vehicle_timestamp'|time of reporting status by train|
|'vehicle_stop_id'|stop id when reporting status|
|'weekday'|weekday|
|'trip_id2'|reconstructed trip id|
|'match_id'|unique id for matching arrivals and schedules.



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
### MTA GTFS Dictionary
- [GTFS-realtime Reference](http://datamine.mta.info/sites/all/files/pdfs/GTFS-Realtime-NYC-Subway%20version%201%20dated%207%20Sep.pdf)

### Web Application
- [subwaystats](http://subwaystats.com/)
- [MTA dashboard](http://dashboard.mta.info/)

## Bias & Limitation
- Sampling process
  - Not all arrival data is uploaded in this MTA real-time system.
  - Abnormal data exists (abnormal time/ trip_id), and they were filtered.
  - Sampling rate reported.
