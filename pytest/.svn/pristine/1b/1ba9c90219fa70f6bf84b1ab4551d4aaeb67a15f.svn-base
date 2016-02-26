from rediscluster import StrictRedisCluster
startup_nodes = [{"host": "192.168.1.168", "port": "7000"}]
rc = StrictRedisCluster(startup_nodes=startup_nodes, decode_responses=True)
ps = rc.pubsub()
ps.subscribe(['foo', 'bar'])
rc.publish('foo', 'hello foo from python')
rc.publish('bar', 'hello bar from python')