from os import getenv
import re
import requests
from bs4 import BeautifulSoup
from persistence import save, read

class UISAuth:
    UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0"

    url_login = 'https://uis.fudan.edu.cn/authserver/login?service=http://jwfw.fudan.edu.cn/eams/home.action'

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
            "service": "http://jwfw.fudan.edu.cn/eams/home.action"
        }

        result = re.findall(
            '<input type="hidden" name="([a-zA-Z0-9\-_]+)" value="([a-zA-Z0-9\-_]+)"/?>', page_login)

        data.update(result)

        headers = {
            "Host": "uis.fudan.edu.cn",
            "Origin": "https://uis.fudan.edu.cn",
            "Referer": self.url_login,
            "User-Agent": self.UA,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Cache-Control": "max-age=0"
        }


        post = self.session.post(
            self.url_login,
            data=data,
            headers=headers,
            allow_redirects=False)

        if post.status_code == 302:
            print(post.text)
            print("Login successfully\n")
        else:
            print("Login failed\n")
            self.close()

    def logout(self):
        exit_url = 'https://uis.fudan.edu.cn/authserver/logout?service=/authserver/login'
        self.session.get(exit_url).headers.get('Set-Cookie')

    def close(self):
        self.logout()
        self.session.close()


def get_account():
    uid = getenv("STD_ID")
    psw = getenv("PASSWORD")
    if uid != None and psw != None:
        return uid, psw


class GradeChecker(UISAuth):
    def __init__(self, uid, password):
        super().__init__(uid, password)
        self.gpa_table = []
        self.my_gpa = 0.0
        self.mid = 0.0
        self.avg = 0.0

    def req(self):
        res = self.session.post("https://jwfw.fudan.edu.cn/eams/myActualGpa!search.action")

        if "重复登录" in res.text:
            soup = BeautifulSoup(res.text, 'html.parser')
            href = soup.find('a')['href']
            res = self.session.post(href)

        soup = BeautifulSoup(res.text, 'html.parser')
        rows = soup.find_all('tr')
        
        for row in rows[1:]:
            columns = row.find_all('td')
            row_data = [col.get_text() for col in columns]
            self.gpa_table.append(row_data)
    
    def stat(self):
        for r in self.gpa_table:
            self.avg += float(r[5])
            if r[0] != '****':
                self.my_gpa = float(r[5])
        self.avg = self.avg / len(self.gpa_table)
        self.mid = float(self.gpa_table[int(len(self.gpa_table) / 2)][5])
        return self.my_gpa, self.avg, self.mid
            
        
if __name__ == '__main__':
    uid, psw = get_account()
    gc = GradeChecker(uid, psw)
    gc.login()
    gc.req()
    my_gpa, avg, mid = gc.stat()
    print(my_gpa)
    gc.close()
    old_my, old_avg, old_mid = read(psw)
    if old_my != my_gpa:
        save(my_gpa, avg, mid, psw)
        token = getenv("TOKEN")
        title = "GPA changed: " + str(my_gpa) + " "
        url = "http://www.pushplus.plus/send?token=" + token + "&title=" + title + "&content=" + "&template=html"
        requests.get(url)
