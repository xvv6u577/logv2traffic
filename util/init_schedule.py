import schedule
import time
from tinydb import TinyDB, Query

from util import traffics_util

db= TinyDB('db.json')
db_users = db.table('users')

def get_traffic_data_to_db():

    stats, moment = traffics_util.get_traffic()

    for stat in stats:
        # 新用户流量，新建用户信息
        if 'user' == stat['id_type']:
            if [] == db_users.search(Query().email == stat['tag']):
                db_users.insert({
                    "email": stat['tag'],
                    "path": "",
                    "uuid": ""
                })

        inbound = db.table(stat['tag'])
        if 0 == stat['uplink'] and 0 == stat['downlink']:
            inbound.insert({
                moment: 0
            })
        else:
            inbound.insert({
                'timestamp': moment,
                'uplink': stat['uplink'],
                'downlink': stat['downlink']
            })

schedule.every(5).minutes.do(get_traffic_data_to_db)

def start_app():
  while True:
    schedule.run_pending()
    time.sleep(0.2)
