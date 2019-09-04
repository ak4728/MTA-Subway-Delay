def RequestsWrite(APIkey, feed_id):
    '''
    This function takes APIkey and feed_id as an input, and 
    Requests MTA subway real-time status, and Writes a gtfs file.
    '''
    import requests
    url = 'http://datamine.mta.info/mta_esi.php?key=' + APIkey + '&feed_id=' + str(feed_id)

    response = requests.get(url)

    from google.transit import gtfs_realtime_pb2
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(response.content)

    from datetime import datetime
    timestamp = datetime.fromtimestamp(feed.header.timestamp)

    import os
    FolderName = '%02d'%(timestamp.year) + '%02d'%(timestamp.month) + '%02d'%(timestamp.day)
    if not os.path.isdir(FolderName):
        os.mkdir(FolderName)
    file = open(FolderName + "/gtfs_" + str(feed_id) + '_' + str(timestamp).replace(" ", "-").replace(":", "-") + ".gtfs", "wb") # gtfs_2019-09-03-15-42-43.gtfs
    file.write(response.content)
    file.close()

def CollectRealtimeGTFS(APIkey):
    '''
    This function takes APIkey as an input, and 
    Keep requesting MTA subway real-time status, and Writting gtfs files.
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
            RequestsWrite(APIkey, feed_id)

        import time
        time.sleep(3) # Every 5 seconds update; 3 seconds sleep for a loop to make sure the data integrity.
        
if __name__ == "__main__":
    import sys
    APIkey = sys.argv[1]
    CollectRealtimeGTFS(APIkey)