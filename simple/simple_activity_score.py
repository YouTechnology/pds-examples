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
"""Calculate a user's activity score
 
Type: personal
 
Input:
    activity:  /v1/data/tc.you.demo.SimpleActivityType
    old_score:	/v1/data/tc.you.demo.SimpleActivityScore
    

Output:
    out1: /v1/data/tc.you.demo.SimpleActivityScore, POST
    out2: /v1/data/tc.you.demo.SimpleActivityType , PUT
"""
def execute(activity, old_score, *args, **kwargs):
    activityScore = {'name': 'FirstAnswer', 'timestamp' : '2014-08-08T13:14:15Z', 'stringP': 'foo'}
    activityUpdate = {'_id': activity[0]['_id'], 'stringP': 'A new value'}
    return dict(out1=[activityScore], out2=[activityUpdate])
