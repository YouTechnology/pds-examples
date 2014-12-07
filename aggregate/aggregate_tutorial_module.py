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
    # Count the unique PDSs 
    pdss = set([message['pds_pds'] for  message in messages])
    pds_count = len(pdss)

    # Calculate the mean number of SMSs
    mean_count = len(messages) / pds_count

    # Prepare output
    aggregate = {'timestamp': int((time.time() + 0.5) * 1000), 
		 'participantsCount': pds_count,
		 'meanSMSCount': mean_count}
    
    return dict(out1=[aggregate])
