## logv2traffic

一个简单的 v2ray 流量统计程序，用 python 实现。

程序运行之后，每 5 分钟统计一次 v2ray 的流量，记录在 db.json。

### 环境 & 安装

> Ubuntu 18.04.3 LTS / Python 3.6.9 / pip3 9.0.1

```
git clone https://github.com/caster8013/logv2traffic.git
cd ./logv2traffic

python3 -m venv .ven
. .ven/bin/activate

pip3 install -r requirement.txt
chmod +x app.py
```

### 运行

##### 由配置文件 main.json 生成数据库文件 db.json

db.json 包括 users 表，记录用户信息；用户的 email 表，存储用户流量统计；进程表，用来记录进程流量。email 表、进程表中，包括每 5 分钟统计一次的流量数据，分为 uplink 和 downlink 两部分，单位为字节（Byte）。

main.json 包括用户信息（email, uuid，所在进程），由 v2ray 的 config.json 生成，格式如下：

```
{
  "cas": [
    {
      "email": "novah",
      "id": "7f539fee-3f15-46b4-84fc-a00310eb50da"
    },
    {
      "email": "david",
      "id": "8890046b-9472-48ea-add0-89af164b7edd"
    }
  ],
  "ray": [
    {
      "email": "luke",
      "id": "60dcbc2e-febc-47a0-848a-032840d9973d"
    }
  ]
}
```

##### 命令行运行

```
python util/init_db.py
python ./app.py
```

每次新加入用户，更新 main.json 之后，再次运行上面命令行，可以更新 db.json。
由 main.json 生成 db.json 的步骤并不是必需。没有的话，程序依然可以记录 v2ray 的流量，只是 users 表中没有 path 和 uuid。

##### 添加 systemctl 服务，让脚本以服务的方式运行。

```
# 更正by5minutes.service中路径之后，运行下面命令
sudo mv by5minutes.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl start by5minutes.service
sudo systemctl enable dummy.service
```

##### 命令行查询

```
# 输出帮助信息
used.py -h
used.py --help

# 查询数据库中，所有用户最初时间、最新使用时间
used.py -u
used.py --users

# 过去一天，所有用户的流量记录
used.py -l
used.py --list

# -d 后面指定整数天数。-d n，表示查询过去n天，所有用户的流量记录
used.py -d 5
used.py --days 5

# -f(or --from), -t(--to)后面指定一个时间段，10位Unix timestamp，查询时间段内，所有用户的流量记录。没有记录的话，流量为0
used.py --from 1583998020 --to 1584084421
used.py -f 1583998020 -t 1584084421

# -p后面指定整数分钟数。查询所有用户过去n分钟的流量记录
used.py -p 240
used.py --past 240

# -i(--in), -o(--out) 后面分别指定json文件名，把2个db.json文件合并到一个文件
used.py -i march.json -o db.json

```

## 感谢

- [v2ray-core](https://github.com/v2ray/v2ray-core.git)
- [v2-ui](https://github.com/sprov065/v2-ui)

## License

Under [GPLv3](https://www.gnu.org/licenses/gpl-3.0.html)
