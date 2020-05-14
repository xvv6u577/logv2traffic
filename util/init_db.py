import json
from tinydb import TinyDB, where
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware

def init():
    with TinyDB("db.json", storage=CachingMiddleware(JSONStorage)) as db:
        db_users = db.table('users')
        with open('main.json') as file:
            threads = json.load(file)
            for thread in threads:
                # 进程的流量统计表
                db.table(thread)
                    
                for user in threads[thread]:
                    # 有新用户加入，添加到users表，同时新建新用户流量统计表
                    if [] == db_users.search(where('email') == user['email']):
                        db_users.insert({
                            'email': user['email'],
                            'path': thread,
                            'uuid': user['id'],
                        })
                        db.table(user['email'])
                        
                    # 流量统计程序加入的user，更新用户信息
                    else:
                        db_users.upsert({
                            'email': user['email'],
                            'path': thread,
                            'uuid': user['id'],
                        }, where('email') == user['email'])

if __name__ == "__main__":
    init()     