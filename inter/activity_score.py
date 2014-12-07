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
"""Calculates individual activity score for a hourly timebin and normalized against population distribution
   Raw score is incremental throughout a day. Normalization performed against distribution of raw scores for an average full day 
   Uses bisect_left from bisect lib 
    
Type: personal
 
Input:
    stepCounts: /v1/data/PdsPedometer/query/tc.you.demo.PdsPedometer_lastMonth
    stats: /v1/data/tc.you.demo.PedometerStats
Output:
    score: /v1/data/tc.you.demo.LifeStyleActivityScore, POST

"""
import math
import time

# We're assuming a normal distribution for steps.
# This should be a reasonable assumption, but we won't know until we have the data. 
def CDF(x, mean, dev):
    return 0.5 * (1.0 + math.erf(float(x - mean) / (float(dev) * math.sqrt(2)))) if dev <> 0 else -1

def execute(stepCounts, stats, *args, **kwargs):
    # Assuming step counts are returned in descending order of startTime...
    #now = int(time.time()*1000)
    now = 1416960000000 # end of custom query data
    oneDay = 3600*24*1000
    totals = [{ "start": now, "total": 0}, { "start": now - 7*oneDay, "total": 0}, {"start": now - 30*oneDay, "total": 0}]
    stepStarts = [s["startTime"] for s in stepCounts]
    
    # Add step counts to intervals they occur in
    for counts in stepCounts:
        for total in totals:
            if counts["startTime"] > total["start"]:
                total["total"] += counts["steps"]
    
    # Take the most recent personal pedometer stats....
    # This will be scoring yourself relative to yourself, though. Probably not what we want.
    personalStats = max([s for s in stats if s["scoreType"] == "personal"], key = lambda s: s["timestamp"])
    
    # Just taking the CDF for the score
    answer = { "scoreType": "personal", "timestamp": int(time.time()*1000) }
    answer["scoreDay"] = 100.0 * CDF(totals[0]["total"], personalStats["meanDay"], personalStats["devDay"])
    answer["scoreWeek"] = 100.0 * CDF(totals[1]["total"], personalStats["meanWeek"], personalStats["devWeek"])
    answer["scoreMonth"] = 100.0 * CDF(totals[2]["total"], personalStats["meanMonth"], personalStats["devMonth"])    
    
    return dict(score=[answer])
    
    
