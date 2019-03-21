import boto3
import csv
import re

 
bucket = 'dotcam'
prefix = 'ID_932_a'
flag = False


def get_all_s3_objects(s3, **base_kwargs):
    continuation_token = None
    while True:
        list_kwargs = dict(MaxKeys=1000, **base_kwargs)
        if continuation_token:
            list_kwargs['ContinuationToken'] = continuation_token
        response = s3.list_objects_v2(**list_kwargs)
        yield from response.get('Contents', [])
        if not response.get('IsTruncated'):  # At the end of the list?
            break
        continuation_token = response.get('NextContinuationToken')

        
 
 
 
with open(prefix +'_size.csv', 'w') as csvfile:
        fieldnames = ['Cam ID',"Date/Time", 'Size (KB)',"Flag"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()        
        
        for file in get_all_s3_objects(boto3.client('s3'), Bucket=bucket, Prefix=prefix):
  
    
        
            
            if file['Size']/1000 > 10:
                flag = True
            else:
                flag = False
            keys = list(filter(None, re.split('_', file['Key'])))
            id = keys[1]
            datetime =  keys[-1][:-4]
            writer.writerow({'Cam ID': id,"Date/Time":datetime, 'Size (KB)': float(file['Size'])/1000, "Flag":  flag})
