import json
import time
import re
import requests
from sys import exit as sys_exit
from os import getenv
from bs4 import BeautifulSoup
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings


class UISAuth:
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
            print("Login successfully\n")
        else:
            print("Login failed\n")
            self.close()

    def logout(self):
        exit_url = 'https://uis.fudan.edu.cn/authserver/logout?service=/authserver/login'
        expire = self.session.get(exit_url).headers.get('Set-Cookie')

    def close(self, exit_code=0):
        self.logout()
        self.session.close()
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


# Find a course that has just released
# Notice: we suppose that there will be no more than 1 newly released course during the consecutive queries
def find_newly_released_course(pre: dict, new: dict) -> str:
    for i in new.keys():
        if not pre.keys().__contains__(i):
            return i


# Find a course the grade of which has changed since last query
def find_updated_course(pre: dict, new: dict) -> str:
    for i in new.keys():
        if pre[i] != new[i]:
            return i


# Due to a curious bug(?) of the push platform we choose(for the grade "B+", the "+" will not show), we adopt a gpa_table to address this issue.
gpa_table = {
    "A": "4.0",
    "A-": "3.7",
    "B+": "3.3",
    "B": "3.0",
    "B-": "2.7",
    "C+": "2.3",
    "C": "2.0",
    "C-": "1.7",
    "D": "1.3",
    "D-": "1.0",
    "F": "F",
    "P": "P",
    "NP": "NP"
}


class GradeChecker(UISAuth):
    def get_new_course(self):
        res = self.session.get("https://my.fudan.edu.cn/list/bks_xx_cj")
        soup = BeautifulSoup(res.text)
        td = soup.find("tbody").find_all("td")
        current_course_record: dict = {}

        for i in range(3, len(td), 6):
            name = td[i].text
            current_course_record[name] = td[i + 2].text

        with open('record.json', 'r+') as f:
            previous_data: dict = json.load(f)
            time.sleep(0.1)
            if len(previous_data) < len(current_course_record.keys()):
                newly_released_course = find_newly_released_course(previous_data, current_course_record)
                json.dump(current_course_record, f)
                return gpa_table[str(current_course_record[newly_released_course])] + newly_released_course
            elif len(previous_data) == len(current_course_record.keys()):
                updated_course = find_updated_course(previous_data, current_course_record)
                json.dump(current_course_record, f)
                return gpa_table[str(current_course_record[updated_course])] + updated_course


if __name__ == '__main__':
    disable_warnings(InsecureRequestWarning)
    requests.adapters.DEFAULT_RETRIES = 5
    uid, psw = get_account()
    grade_checker = GradeChecker(uid, psw)
    grade_checker.login()
    new_course = grade_checker.get_new_course()
    if not new_course == "None":
        token = getenv("TOKEN")
        title = "出分: " + new_course
        url = "http://www.pushplus.plus/send?token=" + token + "&title=" + title + "&content=" + "&template=html"
        requests.get(url)
