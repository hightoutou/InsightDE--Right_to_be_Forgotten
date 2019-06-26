#!/usr/bin/python3.6

#####################################
# split the whole files into smaller files
#####################################

# Read data from S3
import boto3
import io
import numpy as np
import pandas as pd
s3 = boto3.client('s3') #low-level functional API

fname = 'users_all'
n = 10

obj = s3.get_object(Bucket='airbnbbookingwqk', Key=fname+'.csv')
df = pd.read_csv(io.BytesIO(obj['Body'].read()), sep = '\t', header=None)

# Split the df
df_split = np.array_split(df, n)

# Write df to S3

from io import StringIO # python3
s3_resource = boto3.resource('s3')

for i in range(n):
    csv_buffer = StringIO()
    df_split[i].to_csv(csv_buffer, sep = '\t', header=None, index=False)
    s3_resource.Object('airbnbbookingwqk', fname+'_'+str(i+1)+'.csv').put(Body=csv_buffer.getvalue())


