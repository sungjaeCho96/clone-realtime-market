import asyncio
import json
import websockets
from quotation import Quotation

import redis

redis_pool = redis.ConnectionPool(host="127.0.0.1", port=6379, db=0, max_connections=4)

MSG = [
  {"ticket": "test"},
  {
    "type": "ticker",
    "codes": Quotation().get_market("KRW"),
    "isOnlyRealtime": True
  },
]

DATA = json.dumps(MSG)

async def connect_socket():
  with redis.StrictRedis(connection_pool=redis_pool) as conn:
    while True:
      print("outer loop")
      try:
        async with websockets.connect("wss://api.upbit.com/websocket/v1", ping_interval=None, ping_timeout=30, max_queue=10000) as wsocket:
          await wsocket.send(DATA)
          while True:
            print("inner loop")
            try:
              res = await wsocket.recv()
              data = json.loads(res)
              
              if "code" not in data:
                print(f"[DATA erro] : {data}")
                continue
              
              ticker = data["code"].split("-")[-1]
              conn.set(ticker, res)
              # print(f"{ticker} : {data}")
            except (asyncio.TimeoutError, websockets.exceptions.ConnectionClosed):
              try:
                pong = await wsocket.ping()
                await asyncio.wait_for(pong, timeout=30)
              except:
                await asyncio.sleep(30)
                break
            except:
              import traceback
              traceback.print_exc()
      except:
        await asyncio.sleep(30)
      
async def run():
  await asyncio.wait([
    asyncio.create_task(connect_socket())
  ])
  
if __name__ == "__main__":
  asyncio.run(run())