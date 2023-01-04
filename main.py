import json
import re
import requests
from sys import exit as sys_exit
from os import getenv
from bs4 import BeautifulSoup

requests.adapters.DEFAULT_RETRIES = 5

class Fudan:
    UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0"

    url_login = 'https://uis.fudan.edu.cn/authserver/login?service=https://my.fudan.edu.cn/list/bks_xx_cj'

    def __init__(self, uid, password):
        self.session = requests.session()
        self.session.keep_alive = False
        self.session.headers['User-Agent'] = self.UA
        self.uid = uid
        self.psw = password

    def _page_init(self):
        page_login = self.session.get(self.url_login)
        if page_login.status_code == 200:
            return page_login.text
        else:
            self.close()

    def login(self):
        page_login = self._page_init()

        data = {
            "username": self.uid,
            "password": self.psw,
            "service": "https://my.fudan.edu.cn/list/bks_xx_cj"
        }

        result = re.findall(
            '<input type="hidden" name="([a-zA-Z0-9\-_]+)" value="([a-zA-Z0-9\-_]+)"/?>', page_login)

        data.update(result)

        headers = {
            "Host": "uis.fudan.edu.cn",
            "Origin": "https://uis.fudan.edu.cn",
            "Referer": self.url_login,
            "User-Agent": self.UA
        }

        post = self.session.post(
            self.url_login,
            data=data,
            headers=headers,
            allow_redirects=False)

        if post.status_code == 302:
            print("登录成功\n")
        else:
            print("登录失败，请检查账号信息")
            self.close()

    def logout(self):
        exit_url = 'https://uis.fudan.edu.cn/authserver/logout?service=/authserver/login'
        expire = self.session.get(exit_url).headers.get('Set-Cookie')

        if '01-Jan-1970' in expire:
            print("登出完毕")
        else:
            print("登出异常")

    def close(self, exit_code=0):
        self.logout()
        self.session.close()
        print("关闭会话")
        sys_exit(exit_code)


def get_account():
    uid = getenv("STD_ID")
    psw = getenv("PASSWORD")
    if uid != None and psw != None:
        print("从环境变量中获取了用户名和密码！")
        return uid, psw


class Course:
    def __init__(self, name, grade):
        self.name = name
        self.grade = grade


def compare_records(pre: dict, new: dict) -> str:
    for i in new.keys():
        if not pre.keys().__contains__(i):
            return i


class GradeChecker(Fudan):
    def get_new_course(self):
        res = self.session.get("https://my.fudan.edu.cn/list/bks_xx_cj")
        soup = BeautifulSoup(res.text)
        td = soup.find("tbody").find_all("td")
        course_record: dict = {}

        for i in range(3, len(td), 6):
            name = td[i].text
            course_record[name] = td[i + 2].text

        with open('record.json', 'r') as f:
            previous_data: dict = json.load(f)

        if len(previous_data) < len(course_record.keys()):
            new_course = compare_records(previous_data, course_record)
            with open('record.json', 'w') as f:
                json.dump(course_record, f)
            return new_course + " " + str(course_record[new_course])
        else:
            return "None"


if __name__ == '__main__':
    uid, psw = get_account()
    grade_checker = GradeChecker(uid, psw)
    grade_checker.login()
    new_course = grade_checker.get_new_course()
    if not new_course == "None":
        token = getenv("TOKEN")
        title = "出分: " + new_course
        url = "http://www.pushplus.plus/send?token=" + token + "&title=" + title + "&content=" + "1" + "&template=html"
        requests.get(url)
