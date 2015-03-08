# Copyright 2014 You Technology, Inc. or its affiliates. All Rights Reserved.
# 
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
# 
#     http://www.apache.org/licenses/LICENSE-2.0.html
# 
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.
"""This is a 3nd iteration  of a module which: Computes Points of Interest
   This work is based on Andrea Cuttone's thesis from DTU IMM <citation>
   At this point it:
       resamples every 15 minutes
       takes highg haccuracy data  (acc < 60)
       Assumes cleaned up data
   V 0.31 : added timezone support (madule works also with missing tz data)    
       

Type: personal
 
Input:
    
    locations : /v1/data/PdsLocation/query/tc.you.demo.PdsLocation_acc60_last27h
 
Output:
    newStops: /v1/data/tc.you.demo.StopLocationsDay, POST



"""
from math import radians, cos, sin, asin, sqrt
import pandas as pd
from sklearn.cluster import DBSCAN
import time,datetime

#ancillary functions
def haversine(lon1, lat1, lon2, lat2):
    """computes great circle distance between two points given lon lat
    In: lon lat cordinates of 2 points
    Out: distance in meters
    """
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    #average radius of Earth in meters is 6371000, I'm using 6367000 after Andrea cos he uses differnt fromula for c (which I don)
    distance_in_meters = 6367000 * c
    return distance_in_meters

def haversine_metric(a, b):
    """ ancilary metrica for the DBSCAN
    It tells DBSCAN how to calculate distance
    In: lon lat of two points given as a separate list or touple per point
    """
    if len(a) == 2 and len(b) == 2:
        return haversine(lon1=a[0], lat1=a[1], lon2=b[0], lat2=b[1])
    else:    
        return 0

    
def load_data_to_df(pds_locations_list):
    """Loads pds database location data into a pandas dataframe.
    Loop over each record (element of array) and extracts the lon, lat and timestamp.
    Does not filter anything, assumes filtering done on the level of query or after loading into DF.
    In: PdsLocation list with at least coordinates and timestamp properties
    Out: pandas dataframe 3 columns: lon, lat, timestamp, without a proper index
    """
    rows = []
    for location in pds_locations_list:
        # row contains lon lat timestamp
        row = []
        row.extend(location['coordinates']['coordinates'])
        row.append(location['timestamp']) 
        row.append(location.get('tz'))

        rows.append(row)        
    locations_df = pd.DataFrame(rows, columns=['lon','lat','timestamp','tz'])
    locations_df['timestamp'] = pd.to_datetime(locations_df['timestamp'],unit='ms')
    return locations_df
#ancillary function grouping consecutive readouts (achieved by iteration over readouts) within a 60m radius (achieved by distanceCondiditonF)


def resample_locations (location_df):
    """Resamples loaded data to 15 minute intervals to achieve times series
    Resamples using pandas dataframe methods resample on a dataframe indexed by datetime
    Im: locations dataframe (with timestamp in datetime format)
    Out: dataframe resampled to 15 mins intervals
    """
    resampled_df = location_df.set_index('timestamp').resample('15min', how='median').dropna(subset=location_df.columns[0:2]) 
    resampled_df['timestamp'] = resampled_df.index
    return resampled_df

def group_locations(locations_df, distanceCondiditonF):
    """Groups records into logical locations. Assumes time sorted data.
    Searches chronologically: starts with first points, constructs a group around it from later records found within a given 
    radius (60 m at the moment).
    If a records is found outside the radius it starts a new group.
    Takes a distance condidion checking function as input (we can possibly simplyfy it as we wont be checking different functions probably) 
    In: locations dataframe, distance condition testing function
    Out: list of groups, where group is a separate dataframe 
    """
    groups = []
    i = 0

    while i < len(locations_df):
        #start each iteration from the value of main iterator
        j = i
        #iterates untill last but one row of data frame and another essential condition !!!  <----
        #
        while j < len(locations_df) - 1 and distanceCondiditonF(i, j + 1):
                #increment iterator
                j = j + 1
        #adds a group wich is the dataframe slice from the start iterator i to next iterator j
        #uses append so new group is a df with all member locations
        groups.append(locations_df.iloc[i:j + 1])
        i = j + 1
    return groups

################################################################# main function

def execute(locations, *args, **kwargs):
    if len(locations) == 0: return {'newStops':[]}   

    # grouping , stop and clustering parameters declaration
    group_radius = 60        
    min_time_spent_in_stop = 60  #sec
    clustering_distance = 60
    
    #load data to a dataframe and resample to 15 min intervals
    # Note... this does not scale over large input sets.  To make ths work we would need to
    # process the data in fixed sized batches to ensure we don't consume too much memory.
    locations_df = load_data_to_df(locations)
    resampled_df = resample_locations(locations_df)

    #pools locations into chronological groups of radious 60m (group_radius) (hardcode this lambda into group_locations)
    #haversine (start, next  ) start and next refer to the integer values passed by group_locations function 
    groups = group_locations(resampled_df, lambda first_location, next_location: 
        haversine(resampled_df['lon'].values[first_location],resampled_df['lat'].values[first_location], 
        resampled_df['lon'].values[next_location],resampled_df['lat'].values[next_location]) <= group_radius)
    
    # filter the stop locations ie. locations with time spent > min_imte_spent_in_stop witch is 1 minute
    stop_locations = []
    values = []
    for group in groups:
        # median lon, lat for group and first, last timestamps
        values.append([group.lon.median(), group.lat.median(), group.timestamp.values[0], group.timestamp.values[-1], group.tz.min()])
    
    stop_locations = pd.DataFrame(values, columns=['lon', 'lat', 'arrival', 'departure','tz'])
    stop_locations = stop_locations[stop_locations.departure - stop_locations.arrival >= min_time_spent_in_stop]
    
    if len(stop_locations) == 0: return {'newStops':[{'date':datetime.date.today().strftime("%Y-%m-%d")}]}   

    # initialize the DBSCAN object
    db = DBSCAN(eps=60, min_samples=1, metric=haversine_metric)
    #extract coordinates form stop_locations dataframe
    stop_coordinates = stop_locations[['lon', 'lat']].values
    # run the culstering 
    db.fit(stop_coordinates)
    
    ############################################################## preparing the outup for pds
    # quite complex way to convert pandas datetime to epoch millis 
    stop_locations['poiLabel'] = db.labels_
    arrival_tmp = pd.DatetimeIndex(stop_locations['arrival'])
    arrival_tmp = arrival_tmp.to_pydatetime()
    arrival_tmp = map(lambda x: round(time.mktime(x.timetuple())*1000), arrival_tmp)  #converts to epoch
    stop_locations['arrival'] = arrival_tmp
    departure_tmp = pd.DatetimeIndex(stop_locations['departure'])
    departure_tmp  = departure_tmp.to_pydatetime()
    departure_tmp  = map(lambda x: round(time.mktime(x.timetuple())*1000), departure_tmp )  #converts to epoch
    stop_locations['departure'] = departure_tmp

    # change NaN to None
    s_l = stop_locations.where((pd.notnull(stop_locations)), None) 
    
    # convert the df into a list of dictionaires 
    stops_list = [{"coordinates" : {"type": "Point", "coordinates":[float(s_l.iloc[row,0]), float(s_l.iloc[row,1])]}, "arrival":int(s_l.iloc[row,2]), "departure":int(s_l.iloc[row,3]), "tz": s_l.iloc[row,4] ,"poiLabel":int(s_l.iloc[row,5])} for row in range(len(s_l))]
    # convert tz into int
    for stop in stops_list:
        if stop['tz'] is not None:
            stop['tz'] = int(stop['tz'])
        
    answer= {'timestamp': int(time.time()*1000),
	     'date': datetime.date.today().strftime("%Y-%m-%d"),
	     'stops': stops_list
    }
        
    return dict(newStops=[answer])
