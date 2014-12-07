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
