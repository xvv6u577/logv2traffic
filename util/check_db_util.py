from tinydb import TinyDB, where

from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware


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
                user_table = raw_user_table.search(where("timestamp").exists())

                for item in user_table:
                    if _to >= int(item["timestamp"]) >= _from:
                        uplink_total += item["uplink"]
                        downlink_total += item["downlink"]

            stats.append(
                {
                    "user": user["email"],
                    "uplink": uplink_total,
                    "downlink": downlink_total,
                }
            )

    stats.sort(key=lambda i: i["downlink"], reverse=True)

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
