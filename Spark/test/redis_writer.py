import redis

redis_server = 'ec2-52-34-94-103.us-west-2.compute.amazonaws.com'

users = ['ec48p5a22d', 'yiztwgpvgx', 'l1rhqqeko0', 'rd7tfslgsc', 'qnygpy84n6']
rdb = redis.StrictRedis(redis_server, port=6379, db=0, decode_responses=True)
print(users)
print(type(users))
for user in users:
    rdb.append(user, 1)
