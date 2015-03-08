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
"""Simple aggeregate module for training purpsoes

Notice the aggregate in the TYPE field below


Type: aggregate
 
Input:
    messages : /v1/data/PdsSMS
 
Output:
    out1: /v1/data/tc.you.demo.ExampleAggregateType, POST

"""
import time

def execute(messages, *args, **kwargs):
    # Process messages, counting total and noting the unique PDSs.
    # Note that the PDS count won't scale over large input streams...
    msg_count = 0
    pdss = set()
    for msg in messages:
        msg_count += 1
        pdss.add(msg['pds_pds'])
    
    # Calculate the mean number of SMSs
    pds_count = len(pdss)
    mean_count = msg_count / pds_count

    # Prepare output
    aggregate = {'timestamp': int((time.time() + 0.5) * 1000), 
		         'participantsCount': pds_count,
		         'meanSMSCount': mean_count}
    return dict(out1=[aggregate])
