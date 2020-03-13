import time
from tinydb import TinyDB, where

db= TinyDB('db.json')
db_users = db.table('users')

# 返回过去一天，活动用户的流量统计
def get_days_stats(day = 1):

  now = int(time.time())
  past_one_day = now - 86400 * day
  info = []

  for user in db_users:
    uplink_total = 0
    downlink_total = 0
    raw_user_table = db.table(user['email'])
    user_table = raw_user_table.search(where('timestamp').exists())

    for item in user_table:
      if now >= int(item['timestamp']) >= past_one_day :
          uplink_total += item['uplink']
          downlink_total += item['downlink']

    info.append({
      'user': user['email'],
      'uplink': uplink_total,
      'downlink': downlink_total
    })

  info.sort(key = lambda i:i['downlink'], reverse = True)
  
  return info, past_one_day, now

def get_users_info():
  info = []
  for user in db_users:
    timestamp = 0
    u = db.table(user['email'])
    if len(u) >0:
      # list(u.all()[0].keys())[0] - get key at {'1583841550': 0}
      timestamp = int(list(u.all()[0].keys())[0]) \
        if len(u.all()[0]) == 1 else int(u.all()[0]['timestamp'])
    info.append({
      'timestamp': timestamp,
      'user': user['email']
    })
  info.sort(key = lambda i:i['timestamp'], reverse = True)

  return info