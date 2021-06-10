from tinydb import TinyDB, where

from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware
import datetime

def traffic_by_month(month = 0, year = 0):
    months = [1,2,3,4,5,6,7,8,9,10,11,12]
    if 0 == year:
        year = datetime.datetime.now().year
    if month in months:
        if 12 == month:
             start, end = int(datetime.datetime(year, month, 1).timestamp()), int(datetime.datetime(year + 1, 1, 1).timestamp())
        else:
            start, end = int(datetime.datetime(year, month, 1).timestamp()), int(datetime.datetime(year, month + 1, 1).timestamp())
        return get_stats(start, end), start, end
    else:
        print("Error! You should input month in number!")
        return

def db_clear(timestamp):
    with TinyDB("db.json", storage=CachingMiddleware(JSONStorage)) as db:
        users_list = []
        users = db.table("users")
        for u in users:
            users_list.append(u['email'])

        for user in users_list:
            user_table = db.table(user)
            to_remove_docs = [t.doc_id for t in user_table if int(t['timestamp']) < timestamp ]
            user_table.remove(doc_ids=to_remove_docs)

def merge_a_into_b(merge, into):
    with TinyDB("db.json", storage=CachingMiddleware(JSONStorage)) as db:
        users = db.table("users")
        if users.search(where('email') == merge) == [] :
            print('Failed!', merge, "doesn't exist!")
            return

        into_doc = users.search(where('email')==merge)
        into_doc[0]['email'] = into

        if users.search(where('email') == into) == []:
            users.insert(into_doc[0])
        else :
            users.upsert(into_doc[0], where('email')==into)

        merge_table = db.table(merge)
        into_table = db.table(into)
        into_table.insert_multiple(merge_table.all())

        doc = users.get(where('email') == merge)
        users.remove(doc_ids=[doc.doc_id])
        db.drop_table(merge)
        
    print('Success!', merge, 'merged into', into)

def user_reset(user):
    with TinyDB("db.json", storage=CachingMiddleware(JSONStorage)) as db:
        users = db.table("users")
        users.remove(where('email') == user)
        db.drop_table(user)

    print('Success! user', user, 'info and traffic table removed!')
    

def db_merge(input, out="db.json"):

    with TinyDB(out, storage=CachingMiddleware(JSONStorage)) as out_db:
        out_users = out_db.table("users")
        with TinyDB(input, storage=CachingMiddleware(JSONStorage)) as in_db:
            in_db_users = in_db.table("users")
            for user in in_db_users:
                if user not in out_users.all():
                    in_db_users.insert(user)
                in_raw_user = in_db.table(user["email"])
                out_raw_user = out_db.table(user["email"])
                out_raw_user.insert_multiple(in_raw_user.all())


def get_stats(_from=0, _to=0):
    if 0 == _to or (_from == _to):
        return []

    stats = []

    with TinyDB("db.json", storage=CachingMiddleware(JSONStorage)) as db:
        db_users = db.table("users")

        for user in db_users:
            uplink_total = 0
            downlink_total = 0
            raw_user_table = db.table(user["email"])

            if 0 == len(raw_user_table):
                uplink_total = -1
                downlink_total = -1
            else:
                for item in raw_user_table:
                    if _to >= int(item["timestamp"]) >= _from:
                        uplink_total += item["uplink"]
                        downlink_total += item["downlink"]

            stats.append( { "user": user["email"], "uplink": uplink_total, "downlink": downlink_total, } )
    stats.sort(key=lambda i: i["downlink"], reverse=True)

    up_final = down_final = 0
    for item in stats:
        up_final += item['uplink']
        down_final += item['downlink']
    
    stats.append( { "user": "Total", "uplink": up_final, "downlink": down_final, } )

    return stats


def get_users_info():
    info = []
    with TinyDB("db.json", storage=CachingMiddleware(JSONStorage)) as db:
        db_users = db.table("users")
        for user in db_users:
            begin = end = 0
            u = db.table(user["email"])
            u_len = len(u)

            if u_len > 0:
                first = u.all()[0]
                last = u.all()[u_len - 1]

                # list(first.keys())[0] - get key at {'1583841550': 0}
                begin = (
                    int(list(first.keys())[0])
                    if len(first) == 1
                    else int(first["timestamp"])
                )
                end = (
                    int(list(last.keys())[0])
                    if len(last) == 1
                    else int(last["timestamp"])
                )
            info.append({"user": user["email"], "begin": begin, "end": end})

    info.sort(key=lambda i: i["end"], reverse=True)

    return info
