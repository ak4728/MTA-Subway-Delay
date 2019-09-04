# MTA Subway Delays
This is a repository for collecting real-time data from the MTA Developer API to compute subway delays at each station.

## Requirements
- python libraries: requests, os, datetime, time, gtfs-realtime-bindings  

If you did not prepare the dependent libraries, please run codes below in Terminal:  
```
pip install --upgrade requests, os, datetime, time, gtfs-realtime-bindings
```

## Installation
```
pip install git+https://github.com/ak4728/MTA-Subway-Delay.git
```

## Usage
### Terminal
#### Execution
1. Open Terminal
2. ```python MTAGTFS.py```
3. Input MTA SUBWAY API KEY

#### Exit
To stop your program, just press ```Control + C```.

### Jupyter Notebook
```
import MTAGTFS
APIkey = 'YOUR MTA SUBWAY API KEY'
```
```
MTAGTFS.CollectRealtimeGTFS(APIkey)
```
## Data Source
### Schedules
- MTA PDF Schedules : https://new.mta.info/schedules
- MTA GTFS data : http://web.mta.info/developers/data/nyct/subway/google_transit.zip
- OpenMobilityData GTFS: https://transitfeeds.com/p/mta/79

### Actual Arrivals
#### Real-time GTFS
- MTA Portal: https://new.mta.info/
- MTA Application: http://subwaytime.mta.info/
- OpenMobilityData: https://transitfeeds.com/p/mta/234

MTA API: http://datamine.mta.info/list-of-feeds

#### GTFS Records
- MTA Data Feeds: http://web.mta.info/developers/developer-data-terms.html#data
- B-Division (Letter trains): http://web.mta.info/developers/data/archives.html
- A-Division (Numeric trains): http://web.mta.info/developers/MTA-Subway-Time-historical-data.html  
                               https://datamine-history.s3.amazonaws.com/index.html
## Reference
### Web Application
- subwaystats: http://subwaystats.com/
- MTA dashboard: http://dashboard.mta.info/

### MTA GTFS Dictionary
- http://datamine.mta.info/sites/all/files/pdfs/GTFS-Realtime-NYC-Subway%20version%201%20dated%207%20Sep.pdf
