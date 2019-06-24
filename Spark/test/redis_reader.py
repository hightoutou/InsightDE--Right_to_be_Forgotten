import redis

redis_server = 'ec2-52-34-94-103.us-west-2.compute.amazonaws.com'

rdb = redis.StrictRedis(redis_server, port=6379, db=0, decode_responses=True)
users_deletion = set()
cursor = '0'
while cursor != 0:
    cursor, keys = rdb.scan(cursor=cursor)
    values = rdb.mget(*keys)
    users_deletion.update([value for value in values if value is not None])
print(users_deletion)
