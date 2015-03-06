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

    # Get output channel
    important_poi = kwargs['importantPoi']

    # Iterate over the stop locations
    for stops in recent_stops:
        # Process all of the recorded stops in this record
	    total_time = defaultdict(int)
	    estimates = defaultdict(list)
        for el in stops['stops]:
		    total_time[el['poiLabel']] += el['departure'] - el['arrival']
		    estimates[el['poiLabel']].append(el['coordinates']['coordinates'])

        # Find the one with the greatest total time
	    sorted_total = sorted(total_time.items(), key=operator.itemgetter(1), reverse=True)
	    homelabel = sorted_total[0][0]
	    estimates = np.array(estimates[homelabel])

        # Create result and write the channel
	    result['coordinates'] = {'type':'Point'}
	    result['coordinates']['coordinates'] = [np.median(estimates[:,0]), np.median(estimates[:,1])]
	    result['poiLabel'] = homelabel
	    result['total_time'] = sorted_total[0][1]
        important_poi.write(result)
