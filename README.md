# douyin_favorite


> 请在python3下运行

这是一个Python的脚本，实时监控抖音用户的作品，喜欢，关注与粉丝数量变化，并使用邮箱通知。

可实时监控你想要观测的用户的抖音时间。

默认间隔为10分钟。

## 环境安装与配置

确定pip -V是python3版
```bash
pip install -r requirements.txt
```
配置脚本中的发送邮箱与接收邮箱，接受邮箱为列表格式，可有多个接收邮箱。

数据库为Mongodb，需要自主安装，[CentOS安装Mongodb](https://www.jianshu.com/p/8e3f4d591b64)

## 运行
```bash
python3 douyin_favorite.py -u https://www.iesdouyin.com/share/user/75459111811
```
## url获取方法

抖音分享后，使用浏览器打开，此时URL则为share/user/id格式

## 实例
<p align="center"><img src="https://raw.githubusercontent.com/piaolin/douyin_favorite/master/picture/shot.jpg" width="1200"></p>
