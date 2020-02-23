import requests
import re
import pymongo
import time
import sys
import optparse
from prettytable import PrettyTable
from smtplib import SMTP
from email.mime.text import MIMEText
from email.header import Header
from apscheduler.schedulers.background import BackgroundScheduler

FROMEMAIL = "pianlin_ying@163.com"
TOEMAIL = ["1418676300@qq.com", ]
STMPSERVER = "smtp.163.com"
EMAILPASS = "16320001222ww"
LASTTIME = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

ENABLEEMAIL = True  # enable email to user

HEADERS = {
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'upgrade-insecure-requests': '1',
    'user-agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
}

Font2Num = {
    'num_': '1',
    'num_1': '0',
    'num_2': '3',
    'num_3': '2',
    'num_4': '4',
    'num_5': '5',
    'num_6': '6',
    'num_7': '9',
    'num_8': '7',
    'num_9': '8'
}

Code2Font = {
    "0xe602": "num_",
    "0xe603": "num_1",
    "0xe604": "num_2",
    "0xe605": "num_3",
    "0xe606": "num_4",
    "0xe607": "num_5",
    "0xe608": "num_6",
    "0xe609": "num_7",
    "0xe60a": "num_8",
    "0xe60b": "num_9",
    "0xe60c": "num_4",
    "0xe60d": "num_1",
    "0xe60e": "num_",
    "0xe60f": "num_5",
    "0xe610": "num_3",
    "0xe611": "num_2",
    "0xe612": "num_6",
    "0xe613": "num_8",
    "0xe614": "num_9",
    "0xe615": "num_7",
    "0xe616": "num_1",
    "0xe617": "num_3",
    "0xe618": "num_",
    "0xe619": "num_4",
    "0xe61a": "num_2",
    "0xe61b": "num_5",
    "0xe61c": "num_8",
    "0xe61d": "num_9",
    "0xe61e": "num_7",
    "0xe61f": "num_6",
    "0xe602": "num_",
    "0xe603": "num_1",
    "0xe604": "num_2",
    "0xe605": "num_3",
    "0xe606": "num_4",
    "0xe607": "num_5",
    "0xe608": "num_6",
    "0xe609": "num_7",
    "0xe60a": "num_8",
    "0xe60b": "num_9",
    "0xe60c": "num_4",
    "0xe60d": "num_1",
    "0xe60e": "num_",
    "0xe60f": "num_5",
    "0xe610": "num_3",
    "0xe611": "num_2",
    "0xe612": "num_6",
    "0xe613": "num_8",
    "0xe614": "num_9",
    "0xe615": "num_7",
    "0xe616": "num_1",
    "0xe617": "num_3",
    "0xe618": "num_",
    "0xe619": "num_4",
    "0xe61a": "num_2",
    "0xe61b": "num_5",
    "0xe61c": "num_8",
    "0xe61d": "num_9",
    "0xe61e": "num_7",
    "0xe61f": "num_6",
    "0xe602": "num_",
    "0xe603": "num_1",
    "0xe604": "num_2",
    "0xe605": "num_3",
    "0xe606": "num_4",
    "0xe607": "num_5",
    "0xe608": "num_6",
    "0xe609": "num_7",
    "0xe60a": "num_8",
    "0xe60b": "num_9",
    "0xe60c": "num_4",
    "0xe60d": "num_1",
    "0xe60e": "num_",
    "0xe60f": "num_5",
    "0xe610": "num_3",
    "0xe611": "num_2",
    "0xe612": "num_6",
    "0xe613": "num_8",
    "0xe614": "num_9",
    "0xe615": "num_7",
    "0xe616": "num_1",
    "0xe617": "num_3",
    "0xe618": "num_",
    "0xe619": "num_4",
    "0xe61a": "num_2",
    "0xe61b": "num_5",
    "0xe61c": "num_8",
    "0xe61d": "num_9",
    "0xe61e": "num_7",
    "0xe61f": "num_6",
    "0xe602": "num_",
    "0xe603": "num_1",
    "0xe604": "num_2",
    "0xe605": "num_3",
    "0xe606": "num_4",
    "0xe607": "num_5",
    "0xe608": "num_6",
    "0xe609": "num_7",
    "0xe60a": "num_8",
    "0xe60b": "num_9",
    "0xe60c": "num_4",
    "0xe60d": "num_1",
    "0xe60e": "num_",
    "0xe60f": "num_5",
    "0xe610": "num_3",
    "0xe611": "num_2",
    "0xe612": "num_6",
    "0xe613": "num_8",
    "0xe614": "num_9",
    "0xe615": "num_7",
    "0xe616": "num_1",
    "0xe617": "num_3",
    "0xe618": "num_",
    "0xe619": "num_4",
    "0xe61a": "num_2",
    "0xe61b": "num_5",
    "0xe61c": "num_8",
    "0xe61d": "num_9",
    "0xe61e": "num_7",
    "0xe61f": "num_6"
}


class DouyinHandle(object):
    def __init__(self, url):
        self.url = url
        self.follower_count = None
        self.favorite_count = None
        self.star_count = None
        self.ID = None
        self.works_count = None

        self.getCode()
        self.update()

    def getCode(self):
        """
        getNumCode from user's page
        """
        s = requests.session()
        r = s.get(self.url, headers=HEADERS)
        shortid = re.findall(r'<p class="shortid">(.*?)</p>', r.text)[0]
        Id_Code = re.findall(
            r'<i class="icon iconfont "> &#(.*?); </i>', shortid)

        star = re.findall(r'<span class="num">(.*?)</span>', r.text)[0]
        Star_Code = re.findall(
            r'<i class="icon iconfont follow-num"> &#(.*?); </i>', star)

        follower = re.findall(
            r'<span class="follower block">(.*?)</span>', r.text)[0]
        Follower_Code = re.findall(
            r'<i class="icon iconfont follow-num"> &#(.*?); </i>', follower)

        works = re.findall(
            r'<div class="user-tab active tab get-list" data-type="post">(.*?)</div>', r.text)[0]
        Works_Code = re.findall(
            r'<i class="icon iconfont tab-num"> &#(.*?); </i>', works)

        favorite = re.findall(
            r'<div class="like-tab tab get-list" data-type="like">(.*?)</div>', r.text)[0]
        favorite_code = re.findall(
            r'<i class="icon iconfont tab-num"> &#(.*?); </i>', favorite)

        self.ID = self.codeToNum(Id_Code)
        self.star_count = self.codeToNum(Star_Code)
        self.follower_count = self.codeToNum(Follower_Code)
        self.works_count = self.codeToNum(Works_Code)
        self.favorite_count = self.codeToNum(favorite_code)

    def codeToNum(self, code_list: list):
        """
        convert douyin code to number
        :param code_list: douyin code list
        :return: number
        """
        codeList = ["0" + i for i in code_list]
        Num = ""
        for i in codeList:
            Num += Font2Num[Code2Font[i]]
        return Num

    def update(self):
        """
        judge the current data and previous data
        """
        # client = pymongo.MongoClient("localhost")
        client = pymongo.MongoClient(
            "mongodb+srv://piaoling:20001222ww@piaolin-2hdvk.azure.mongodb.net/test?retryWrites=true&w=majority")
        db = client.piaolin
        douyin = db.douyin
        if not douyin.count_documents({"url": self.url}):
            douyin.insert_one({"url": self.url, "ID": self.ID, "star_count": self.star_count,
                               "follower_count": self.follower_count, "works_count": self.works_count,
                               "favorite_count": self.favorite_count})
            return
        result = douyin.find_one({"url": self.url})
        douyin.update_one({"url": self.url},
                          {"$set": {"star_count": self.star_count, "follower_count": self.follower_count,
                                    "works_count": self.works_count, "favorite_count": self.favorite_count}})
        if (int(self.star_count) > int(result['star_count']) or
            int(self.follower_count) > int(result['follower_count']) or
            int(self.works_count) > int(result['works_count']) or
            int(self.favorite_count) > int(result['favorite_count'])) and ENABLEEMAIL:
            self.mail(result)

    def mail(self, previous_data):
        """
        send new data to users by e-mail if updated
        :param previous_data: old data
        """
        global LASTTIME
        email_client = SMTP(STMPSERVER)
        email_client.login(FROMEMAIL, EMAILPASS)
        html = """<html>
                <head>
                <style type="text/css">
                table.tftable {font-size:12px;color:#333333;width:100%;border-width: 1px;border-color: #729ea5;border-collapse: collapse;}
                table.tftable th {font-size:12px;background-color:#acc8cc;border-width: 1px;padding: 8px;border-style: solid;border-color: #729ea5;text-align:left;}
                table.tftable tr {background-color:#d4e3e5;}
                table.tftable td {font-size:12px;border-width: 1px;padding: 8px;border-style: solid;border-color: #729ea5;}
                </style>
                </head>
                <body>
                <table id="tfhover" class="tftable" border="1">
                """ + """
                <tr><th>用户名</th><th>作品数</th><th>喜欢数</th><th>关注数</th><th>粉丝数</th><th>时间</th></tr>
                <tr><td>{p[0]}</td><td>{p[1]}</td><td>{p[2]}</td><td>{p[3]}</td><td>{p[4]}</td><td>{p[5]}</td></tr>
                <tr><td>{n[0]}</td><td>{n[1]}</td><td>{n[2]}</td><td>{n[3]}</td><td>{n[4]}</td><td>{n[5]}</td></tr>""".format(
            p=(previous_data['url'], previous_data['works_count'], previous_data['favorite_count'],
               previous_data['star_count'], previous_data['follower_count'], LASTTIME),
            n=(self.url, self.works_count, self.favorite_count, self.star_count, self.follower_count,
               time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))) + """
                </table>
                <script>
                window.onload=function(){
                var tfrow = document.getElementById('tfhover').rows.length;
                var tbRow=[];
                for (var i=1;i<tfrow;i++) {
                tbRow[i]=document.getElementById('tfhover').rows[i];
                tbRow[i].onmouseover = function(){
                this.style.backgroundColor = '#ffffff';
                };
                tbRow[i].onmouseout = function() {
                this.style.backgroundColor = '#d4e3e5';
                };
                }
                };
                </script>
                </body>
                </html>
                """
        print("update:{}".format(LASTTIME))
        tb = PrettyTable()
        tb.field_names = ["id", "works_count", "favorite_count", "star_count", "follower_count", "time"]
        tb.add_row([previous_data['url'], previous_data['works_count'], previous_data['favorite_count'],
                    previous_data['star_count'], previous_data['follower_count'], LASTTIME])  # 添加行数据
        tb.add_row([self.url, self.works_count, self.favorite_count, self.star_count, self.follower_count,
                    time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())])  # 添加列数据
        print(tb)

        msg = MIMEText(html, 'html', 'utf-8')
        msg['Subject'] = Header('抖音用户信息实时监控', 'utf-8')
        msg['From'] = FROMEMAIL
        msg['To'] = ",".join(TOEMAIL)
        email_client.sendmail(FROMEMAIL, TOEMAIL, msg.as_string())
        email_client.quit()

        LASTTIME = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def main(url):
    DouyinHandle(url)


if __name__ == "__main__":

    parser = optparse.OptionParser("Usage: douyin_favorite.py -u <url>", version="V1.0")
    parser.add_option("-u", "--url", action="store", dest="url", default=None,
                      help="e.g.: https://www.iesdouyin.com/share/user/75459111811")
    options, args = parser.parse_args()

    if not options.url:
        parser.print_help()
        sys.exit(2)

    sheduler = BackgroundScheduler()
    sheduler.add_job(main, 'interval', minutes=10, start_date=LASTTIME, args=[options.url])
    sheduler.start()
    try:
        #  This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)
    except(KeyboardInterrupt, SystemExit):
        #  Not strictly necessary if daemonic mode is enabled but should be done if possible
        sheduler.shutdown()
