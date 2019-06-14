# Python 3 codes to shuffle the session stream

# Read data from S3

import boto3
import io
import pandas as pd
s3 = boto3.client('s3') #low-level functional API
obj = s3.get_object(Bucket='airbnbbookingwqk', Key='airbnb-recruiting-new-user-bookings/sessions.csv')
df = pd.read_csv(io.BytesIO(obj['Body'].read()))


# Shuffle all rows

df = df.sample(frac=1).reset_index(drop=True)


# Write new df to s3

from io import StringIO # python3
csv_buffer = StringIO()
df.to_csv(csv_buffer, sep = ' ', header=None, index=False)
s3_resource = boto3.resource('s3')
s3_resource.Object('airbnbbookingwqk', 'sessions_shuffle.csv').put(Body=csv_buffer.getvalue())


