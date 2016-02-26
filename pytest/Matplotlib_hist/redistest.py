# import redis

# r=redis.Redis(host='192.168.1.168',port=6379,db=0)
# r=redis.Redis(host='192.168.1.161',port=7000,db=0)
# print r.info()
# r.set('www','www.sina.com')
# print r.get('www')
#


from rediscluster import StrictRedisCluster
startup_nodes = [{"host": "192.168.1.168", "port": "7000"}]
rc = StrictRedisCluster(startup_nodes=startup_nodes, decode_responses=True)

# rc.set("blog", "http://blog.csdn.net/dgatiger")
# rc.set("www", "http://www.sina.com")
# rc.set("age", "18")
# #rc.save()
# print rc.get('blog')
# print rc.get('www')
# print rc.get('age')
ps=rc.pubsub()
ps.subscribe(['foo', 'bar'])
for item in ps.listen():
    if item['type'] == 'message':
        print item['data']


'''
import redis
rc = redis.Redis(host='127.0.0.1')
ps = rc.pubsub()
ps.subscribe(['foo', 'bar'])
for item in ps.listen():
    if item['type'] == 'message':
        print item['data']

import redis
rc = redis.Redis(host='127.0.0.1')
ps = rc.pubsub()
ps.subscribe(['foo', 'bar'])
rc.publish('foo', 'hello foo')
rc.publish('bar', 'hello bar')
'''