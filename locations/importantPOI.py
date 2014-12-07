
"""At this moment it finds the poi in which the most time was spent and calculates 
	it's estimated location

Type: personal
 
Input:
    
    recent_stops: /v1/data/tc.you.demo.StopLocations/query/tc.you.demo.StopLocations_month
 
Output:
    importantPoi: /v1/data/tc.you.demo.ImportantLocation, POST



"""
import time,datetime
from collections import Counter, defaultdict
import numpy as np
import operator
################################################################# main function

def execute(recent_stops, *args, **kwargs):
	result = {}
	if not recent_stops: return dict(importantPoi=[{}]) # no data to work with 
	recent_stops = recent_stops[0]['stops']
	total_time = defaultdict(int)
	estimates = defaultdict(list)
	for el in recent_stops:
		total_time[el['poiLabel']] += el['departure'] - el['arrival']
		estimates[el['poiLabel']].append(el['coordinates']['coordinates'])

	sorted_total = sorted(total_time.items(), key=operator.itemgetter(1), reverse=True)
	homelabel = sorted_total[0][0]
	estimates = np.array(estimates[homelabel])
	result['coordinates'] = {'type':'Point'}
	result['coordinates']['coordinates'] = [np.median(estimates[:,0]), np.median(estimates[:,1])]
	result['poiLabel'] = homelabel
	result['total_time'] = sorted_total[0][1]
    
	return dict(importantPoi=[result])
