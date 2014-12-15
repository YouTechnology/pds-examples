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
"""Reusing the simple activity score module for the types tutorial
 
Type: personal
 
Input:
    activity:  /v1/data/tc.you.demo.CompilerTest
    old_score:	/v1/data/tc.you.demo.ActivityScore
    

Output:
    out1: /v1/data/tc.you.demo.ExampleType1, POST
    out2: /v1/data/tc.you.demo.ExampleType2, POST

"""
def execute(activity, old_score, *args, **kwargs):
    scalarProperty = []	
    scalarProperty.append({'name': 'Example of a scalar type outupt in "stringP"', 'timestamp' : '2014-08-08T13:14:15Z', 'stringP': '1st SCALAR'})
    scalarProperty.append({'name': 'As you can see you can insert more then one data object at a time, still StringP is a scalar in each of the separate objects', 'timestamp' : '2014-09-09T14:13:11Z', 'stringP': '2st SCALAR'})	

    arrayProperty = {'name': 'Example of an array of scalars in a single property stringProperty. Note that it is still just a single object', 'timestamp' : '2014-11-11T13:14:15Z', 'stringProperty': ['This','is','an','array','of strings']}
    
    
    return dict(out1=scalarProperty, out2=[arrayProperty])
