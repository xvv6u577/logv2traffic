## logv2traffic

一个简单的v2ray流量统计程序，用python实现。

程序运行之后，每5分钟统计一次v2ray的流量，记录在db.json。

### 环境 & 安装

> Ubuntu 18.04.3 LTS / Python 3.6.9 / pip3 9.0.1

```
git clone https://github.com/caster8013/logv2traffic.git
cd ./logv2traffic

python3 -m venv venv
. venv/bin/activate

pip3 install -r requirement.txt
chmod +x app.py
```

### 运行

##### 由配置文件main.json生成数据库文件db.json

db.json包括users表，记录用户信息；用户的email表，存储用户流量统计；进程表，用来记录进程流量。email表、进程表中，包括每5分钟统计一次的流量数据，分为uplink和downlink两部分，单位为字节（Byte）。

main.json包括用户信息（email, uuid，所在进程），由v2ray的config.json生成，格式如下：

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
每次新加入用户，更新main.json之后，再次运行上面命令行，可以更新db.json。
由main.json生成db.json的步骤并不是必需。没有的话，程序依然可以通过v2ray的流量，只是users表中没有path和uuid。

##### 安装supervisor，让脚本以服务的方式运行。

```
sudo apt install supervisor
sudo service supervisor restart

# 移动配置文件之前,更改 app.py 中username为你的用户名：
# #!/usr/bin/env /home/username/logv2traffic/venv/bin/python

# 同样在 by5minutes.conf,指定程序运行目录,更改username为你的用户名：
# directory=/home/username/logv2traffic/
# command=/home/username/logv2traffic/app.py
# user=username

# 把配置文件 by5minutes.conf 放在supervisor的配置文件夹 /etc/supervisor/conf.d/
sudo cp by5minutes.conf /etc/supervisor/conf.d/

sudo supervisorctl reread
sudo supervisorctl update
```

## 感谢

[v2-ui](https://github.com/sprov065/v2-ui)

## License

Under [GPLv3](https://www.gnu.org/licenses/gpl-3.0.html)