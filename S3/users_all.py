# Python 3 codes to shuffle the session stream

# Read data from S3

import pandas as pd
import boto3
from smart_open import smart_open

users = []
for msg in smart_open('s3://airbnbbookingwqk/sessions_shuffle.csv', 'rb'):
    user_id = str(msg, "utf-8").split('\t')[0]
    users.append(user_id)


# Write new df to s3

from io import StringIO # python3
csv_buffer = StringIO()
pd.Series(pd.Series(users).unique()).to_csv(csv_buffer, header=None, index=False)
s3_resource = boto3.resource('s3')
s3_resource.Object('airbnbbookingwqk', 'users_all.csv').put(Body=csv_buffer.getvalue())


