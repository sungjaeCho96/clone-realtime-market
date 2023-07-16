import redis

with redis.StrictRedis(host="127.0.0.1", port=6379, db=0) as conn:
  conn.set("test1", "hello world")
  data = conn.get("test1")
  print(data)
  
redis_pool = redis.ConnectionPool(host="127.0.0.1", port=6379, db=0, max_connections=4)

with redis.StrictRedis(connection_pool=redis_pool) as conn:
  conn.set("test2", "hello 2 world")
  data = conn.get("test2")
  print(data)