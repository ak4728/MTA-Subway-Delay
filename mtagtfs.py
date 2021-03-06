import os
import urllib
import requests
import zipfile
import pandas as pd
import time
from datetime import datetime
from google.transit import gtfs_realtime_pb2
    
def RequestsWrite(APIkey, feed_id):
    '''
    This function takes APIkey and feed_id as an input, and 
    Requests MTA subway real-time status, and Writes a gtfs file.
    '''
    url = 'http://datamine.mta.info/mta_esi.php?key=' + APIkey + '&feed_id=' + str(feed_id)

    response = requests.get(url)

    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(response.content)

    timestamp = datetime.fromtimestamp(feed.header.timestamp)

    FolderName = '%04d'%(timestamp.year) + '%02d'%(timestamp.month) + '/' \
        + '%04d'%(timestamp.year) + '%02d'%(timestamp.month) + '%02d'%(timestamp.day)
    if not os.path.isdir(FolderName):
        os.makedirs(FolderName)
    file = open(FolderName + "/gtfs_" + str(feed_id) + '_' + str(timestamp).replace(" ", "-").replace(":", "-") + ".gtfs", "wb")
    file.write(response.content)
    file.close()

def collect(APIkey):
    '''
    This function takes APIkey as an input, and 
    Keep requesting real-time status for all MTA subway lines, and Writting gtfs files.
    Note: this is an endless loop; to stop this program in terminal, please press Control + C.
    '''    
    feed_id_lines = {'1': '123456S',
                '26': 'ACEHS',
                '16': 'NQRW',
                '21': 'BDFM',
                '2': 'L',
                '11': 'SIR',
                '31': 'G',
                '36': 'JZ',
                '51': '7'
                }
    var = 1
    while var <= 1: # every loop takes about 1 seconds for all 9 feed_id
        for feed_id in feed_id_lines.keys():
            try:
                RequestsWrite(APIkey, feed_id)
            except:
                continue
                
        time.sleep(3) 
        # 15 seconds per update on average (confidence interval between 5 to 30 sec); 
        # 3 seconds sleep (totally less than 5 seconds) for each loop to make sure the data integrity.

def arrival(date):
    '''
    This function takes date(e.g. 20190901) as an input,
    structure and integrate the gtfs files in the corresponding folder,
    output an arrival csv file.
    '''
    errornum = 0
    year, month, day = date[:4], date[4:6], date[6:8]
    FolderPath = year + month + '/' + year + month + day
    gtfsFileNames = os.listdir(FolderPath)
    dict1 = {}
    for gtfsFileName in gtfsFileNames:
        gtfsFilePath = FolderPath + '/' + gtfsFileName
        try:            
            # read in gtfs
            f = open(gtfsFilePath, 'rb')
            raw_str = f.read()
            msg = gtfs_realtime_pb2.FeedMessage()
            msg.ParseFromString(raw_str)    

            # structure gtfs
            gtfs_timestamp = msg.header.timestamp
            for i,entity in enumerate(msg.entity):
                if entity.HasField('trip_update'):
                    try:
                        arrival_time = entity.trip_update.stop_time_update[0].arrival.time
                        stop_id = entity.trip_update.stop_time_update[0].stop_id
                        trip_id = entity.trip_update.trip.trip_id
                        route_id = entity.trip_update.trip.route_id

                        entity2 = msg.entity[i+1]
                        current_stop_sequence = entity2.vehicle.current_stop_sequence
                        current_status = entity2.vehicle.current_status
                        vehicle_timestamp = entity2.vehicle.timestamp
                        vehicle_stop_id = entity2.vehicle.stop_id       

                        dict0 = {'gtfs_timestamp': gtfs_timestamp,
                                'trip_id': trip_id,
                                'arrival_time': arrival_time,
                                'stop_id': stop_id,
                                'route_id': route_id,
                                'current_stop_sequence': current_stop_sequence,
                                'current_status': current_status,
                                'vehicle_timestamp': vehicle_timestamp,
                                'vehicle_stop_id': vehicle_stop_id
                              }                    
                            
                        try: # update record
                            if gtfs_timestamp >= dict1[trip_id+ '//' + stop_id]['gtfs_timestamp']:  
                                dict1[trip_id+ '//' + stop_id] = dict0  
                        except: # add new record
                            dict1[trip_id+ '//' + stop_id] = dict0
                    except:
                        continue
        except: # DecodeError: Error parsing message
            errornum+=1
            continue
    print("%d GTFS files cannot be parsed"%errornum)
    
    df = pd.DataFrame.from_dict(dict1).T.reset_index(drop=True)
    df.to_csv(year + month + '/arrival_' + year + month + day + '.csv')

def delay(date, date_schedule = 'latest'):
    '''
    This function takes date as an input,
    calculate delays by actual arrivals and schedules,
    output a delay csv file.    
    ** require actual arrival/ schedule csv files in the corresponding folder,

    '''
    year, month, day = date[:4], date[4:6], date[6:8]

    #################### Actual Arrival ####################
    df = pd.read_csv(year + month + '/arrival_' + year + month + day + '.csv', index_col=0)

    df.arrival_time = df.arrival_time.apply(lambda x: datetime.fromtimestamp(x))
    df.gtfs_timestamp = df.gtfs_timestamp.apply(lambda x: datetime.fromtimestamp(x))
    df.vehicle_timestamp = df.vehicle_timestamp.apply(lambda x: datetime.fromtimestamp(x))

    weekday_dict = {0:'Weekday', 1:'Weekday', 2:'Weekday', 3:'Weekday', 4:'Weekday', 5:'Saturday', 6:'Sunday'}
    df['weekday'] = df.arrival_time.apply(lambda x: weekday_dict[x.weekday()])

    df['trip_id2'] = df['weekday'] + '-' + df['trip_id']
    df['match_id'] = df['trip_id2'] + '//' + df['stop_id'].astype(str)

    #################### Schedules ####################
    # download schedule gtfs file
    # schedule default setting is the latest; for historical schedule, please refer to: https://transitfeeds.com/p/mta/79
    FolderName = 'schedule_' + date_schedule
    FileName = FolderName + ".zip"
    url = 'https://transitfeeds.com/p/mta/79/' + date_schedule + '/download'
    if not os.path.isdir(FolderName):
        os.makedirs(FolderName)
        urllib.request.urlretrieve(url, FileName)
        with zipfile.ZipFile(FileName, 'r') as zip_ref:
            zip_ref.extractall(FolderName)
            
    stop_times = pd.read_csv(FolderName + "/stop_times.txt")
    stop_times['weekday'] = stop_times.trip_id.apply(lambda x: x.split('-')[-2]) # perfectly extracted
    stop_times['weekday'] = stop_times['weekday'].apply(lambda x: 'Weekday' if x == 'Wednesday' else x) # L train does not have Weekday！ Only ['Saturday', 'Sunday', 'Wednesday']
    stop_times['num_id'] = stop_times.trip_id.apply(lambda x: x.split('_')[1]) # perfectly extracted, fixed lenth
    stop_times['direction'] = stop_times['trip_id'].apply(lambda x: x.split('-')[-1].split('.')[-1][0])
    stop_times['route_id'] = stop_times['trip_id'].apply(lambda x: x.split('_')[-1].split('.')[0])

    stop_times['trip_id2'] = stop_times['weekday'] + '-' + stop_times['num_id'] + '_' + stop_times['route_id'] + '..' + stop_times['direction']
    stop_times['match_id'] = stop_times['trip_id2'] + '//' + stop_times['stop_id']

    stop_times.drop(['stop_headsign', 'pickup_type', 'drop_off_type', 'shape_dist_traveled'], axis=1, inplace=True)
    stop_times.rename(columns={'arrival_time':'arrival_time_scheduled', 'departure_time':'departure_time_scheduled'}, inplace=True)

    # conver timestamp
    stop_times = stop_times[stop_times.arrival_time_scheduled.apply(lambda x: int(x[:2])<24)] # filter abnormal arrival_time which is greater than 24 hour
    stop_times = stop_times[stop_times.arrival_time_scheduled.apply(lambda x: int(x[3:5])<60)] # filter abnormal arrival_time which is greater than 60 minutes
    stop_times.arrival_time_scheduled = pd.to_datetime(stop_times.arrival_time_scheduled.apply(lambda x: year + '-' + month + '-' + day + '-' + x))

    #################### Match ####################
    df_match = pd.merge(df, stop_times[['match_id', 'arrival_time_scheduled', 'departure_time_scheduled']], on='match_id', how='inner')
    df_match['delay'] = (df_match['arrival_time'] - df_match['arrival_time_scheduled']).apply(lambda x: x.total_seconds())
    df_match = df_match[(-60*60*23 < df_match['delay']) & (df_match['delay'] < 60*60*23)] # remove abnomal data
    df_match.reset_index(drop=True, inplace=True)
    df_match.to_csv(year + month + '/delay_' +  year + month + day + '.csv')

if __name__ == "__main__":
    print()
    print('This collect function ceaselessly requesting MTA subway real-time status and writing gtfs files.')
    print('* To stop this program, please press Control + C.')
    
    print()
    APIkey = input('MTA API KEY: ')
    
    print()
    print('Collecting MTA subway gtfs files...')
    collect(APIkey)
