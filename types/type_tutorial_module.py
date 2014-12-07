"""Reusing the simple activity score module for the types tutorial
 
Type: personal
 
Input:
    activity:  /v1/data/tc.you.demo.SimpleActivityType
    old_score:	/v1/data/tc.you.demo.SimpleActivityScore
    

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
