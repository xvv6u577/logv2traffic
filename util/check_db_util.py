from tinydb import TinyDB, where

db = TinyDB('db.json')
db_users = db.table('users')


def get_stats(_from=0, _to=0):
    if 0 == _to or (_from == _to):
        return []

    stats = []
    for user in db_users:
        uplink_total = 0
        downlink_total = 0
        raw_user_table = db.table(user['email'])

        if 0 == len(raw_user_table):
            uplink_total = -1
            downlink_total = -1
        else:
            user_table = raw_user_table.search(where('timestamp').exists())

            for item in user_table:
                if _to >= int(item['timestamp']) >= _from:
                    uplink_total += item['uplink']
                    downlink_total += item['downlink']

        stats.append({
            'user': user['email'],
            'uplink': uplink_total,
            'downlink': downlink_total
        })

    stats.sort(key=lambda i: i['downlink'], reverse=True)

    return stats


def get_users_info():
    info = []
    for user in db_users:
        begin = end = 0
        u = db.table(user['email'])
        if len(u) > 0:
            # list(u.all()[0].keys())[0] - get key at {'1583841550': 0}
            begin = int(list(u.all()[0].keys())[0]) \
                if len(u.all()[0]) == 1 else int(u.all()[0]['timestamp'])
            end = int(list(u.all()[len(u)-1].keys())[0]) \
                if len(u.all()[len(u)-1]) == 1 else int(u.all()[len(u)-1]['timestamp'])
        info.append({
            'user': user['email'],
            'begin': begin,
            'end': end
        })
    info.sort(key=lambda i: i['end'], reverse=True)

    return info
