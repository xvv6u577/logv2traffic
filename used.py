#!/usr/bin/env python3
import sys
import time
import getopt

from util.check_db_util import get_stats, get_users_info, db_merge, merge_a_into_b, user_reset, db_clear
from util.byte_converter import get_printable_size


def echo_stats(info=[], time_from=0, time_to=0):
    print(
        "\nFrom",
        time.asctime(time.localtime(time_from)),
        "to",
        time.asctime(time.localtime(time_to)),
        "\n",
    )
    i = 1
    for item in info:
        if int(item["uplink"]) < 0:
            print("[{:2s}]: {:15s}".format(str(i), item["user"]))
        else:
            print(
                "[{:2s}]: {:15s} uplink {:10s}, downlink {:10s}".format(
                    str(i),
                    item["user"],
                    get_printable_size(item["uplink"]),
                    get_printable_size(item["downlink"]),
                )
            )
        i += 1


def usage():
    print(
        "used.py logv2traffic流量查询工具\n\n",
        "-h --help  输出帮助信息\n",
        "-u --users 查询数据库中，所有用户最初时间、最新使用时间\n",
        "-l --list  过去一天，所有用户的流量记录\n",
        "-d --days  -d,--days 后面指定整数天数。-d n，表示查询过去n天，所有用户的流量记录\n",
        "-f --from, -t --to ",
        "\n            -f(or --from), -t(--to)后面指定一个时间段，10位Unix timestamp，查询时间段内，所有用户的流量记录。没有记录的话，显示为空\n",
        "-p --past  -p,--past后面指定整数分钟数。查询所有用户过去n分钟的流量记录\n",
        "-i(--in)   -o(--out) 后面分别指定json文件名，把2个db.json文件合并到一个文件\n",
        "--merge a --into b 后面分别指定用户名，把a的信息和流量合并到b\n",
        "-r --reset 从数据库中删除用户和流量信息，后跟用户名、指定操作对象\n",
        "--clear 删除指定天数以前的流量统计。后面指定天数，有效值为100~1000以内，100以内更改为100\n",
    )


def entry():
    try:
        # short option with options that require an argument followed ':', like 'o:'
        # long option with options that require an argument followed '=', like "out-file="
        opts, args = getopt.getopt(
            sys.argv[1:],
            "hld:uf:t:p:i:o:r:",
            [
                "help",
                "list-users",
                "out=",
                "days=",
                "users",
                "from=",
                "to=",
                "past=",
                "in=",
                "merge=",
                "into=", 
                "reset=",
                "clear=",
            ],
        )

    except getopt.GetoptError as err:
        print("Error: ", str(err))
        sys.exit(2)

    from_moment = 0
    to_moment = 0
    out = _in = ""
    merge = into = ""

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()

        elif opt in ("--clear"):
            days = 100
            if 1000 > int(arg) > 100:
                days = int(arg)
            db_clear(int(time.time()) - days * 24 * 3600)
            sys.exit()

        elif opt in ("--merge"):
            merge = arg

        elif opt in ("--into"):
            into = arg

        elif opt in ("-i", "--in"):
            _in = arg

        elif opt in ("-o", "--out"):
            out = arg

        elif opt in ("-l", "--list"):
            now = int(time.time())
            past_one_day = now - 86400
            stats = get_stats(past_one_day, now)
            echo_stats(stats, past_one_day, now)
            sys.exit()

        elif opt in ("-d", "--days"):
            now = int(time.time())
            time_from = now - 86400 * int(arg)
            stats = get_stats(time_from, now)
            echo_stats(stats, time_from, now)
            sys.exit()

        elif opt in ("-u", "--users"):
            infos = get_users_info()
            i = 1
            print(
                "\n[{:2s}]: {:15s} {:25s} - {:25s}\n".format(
                    "n", "name", "start", "latest"
                )
            )
            for user_info in infos:
                record_start = record_end = ""
                if 0 != user_info["begin"]:
                    record_start = time.asctime(time.localtime(user_info["begin"]))
                    record_end = time.asctime(time.localtime(user_info["end"]))
                print(
                    "[{:2s}]: {:15s} {:25s} - {:25s}".format(
                        str(i), user_info["user"], record_start, record_end
                    )
                )
                i += 1
            sys.exit()

        elif opt in ("-f", "--from"):
            from_moment = int(arg)
        elif opt in ("-t", "--to"):
            to_moment = int(arg)

        elif opt in ("-p", "--past"):
            now = int(time.time())
            from_moment = now - int(arg) * 60
            infos = get_stats(from_moment, now)
            echo_stats(infos, from_moment, now)
            sys.exit()

        elif opt in ("-r", "--reset"):
            user_reset(arg)
            sys.exit()

    if from_moment and to_moment:
        infos = get_stats(from_moment, to_moment)
        echo_stats(infos, from_moment, to_moment)

    if _in and out:
        db_merge(_in, out)

    if merge and into:
        merge_a_into_b(merge, into)


if __name__ == "__main__":
    entry()
