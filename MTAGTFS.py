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
    file = open(FolderName + "/gtfs_" + str(feed_id) + '_' + str(timestamp).replace(" ", "-").replace(":", "-") + ".gtfs", "wb")
    file.write(response.content)
    file.close()

def CollectRealtimeGTFS(APIkey):
    '''
    This function takes APIkey as an input, and 
    Keep requesting MTA subway real-time status, and Writting gtfs files.
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
                
        import time
        time.sleep(3) 
        # 15 seconds per update on average (confidence interval between 5 to 30 sec); 
        # 3 seconds sleep (totally less than 5 seconds) for each loop to make sure the data integrity.

if __name__ == "__main__":
    APIkey = input('MTA API KEY: ')
    CollectRealtimeGTFS(APIkey)