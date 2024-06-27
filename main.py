from os import getenv
import re
import requests
from bs4 import BeautifulSoup
from cryptography.fernet import Fernet
import base64
import hashlib

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

        if not post.status_code == 302:
            self.close()

    def logout(self):
        exit_url = 'https://uis.fudan.edu.cn/authserver/logout?service=/authserver/login'
        self.session.get(exit_url).headers.get('Set-Cookie')

    def close(self):
        self.logout()
        self.session.close()
        
class Snapshot:
    def __init__(self, gpa=0.0, rank=0.0, credits=0.0, class_avg=0.0, class_mid=0.0):
        self.gpa = gpa
        self.rank = rank
        self.credits = credits
        self.class_avg = class_avg
        self.class_mid = class_mid
    
    def compare(self, another_snapshot):
        if another_snapshot is None:
            return True
        return self.gpa != another_snapshot.gpa or \
            self.rank != another_snapshot.rank or \
                self.credits != another_snapshot.credits
    

class GradeChecker(UISAuth):
    def __init__(self, uid, password):
        super().__init__(uid, password)
        self.login()

    def get_stat(self):
        gpa_table = []
        my_gpa = 0.0
        my_credits = 0.0
        my_rank = 0.0
        class_average = 0.0
        class_mid = 0.0
        
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
            gpa_table.append(row_data)
        
        for _, r in enumerate(gpa_table):
            class_average += float(r[5])
            if r[0] != '****':
                my_gpa, my_credits, my_rank = float(r[5]), float(r[6]), float(r[7])
        
        class_average = class_average / len(gpa_table)
        class_mid = float(gpa_table[int(len(gpa_table) / 2)][5])
        return Snapshot(my_gpa, my_rank, my_credits, class_average, class_mid)
    

def generate_key(password: str) -> bytes:
    hash = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(hash)


def encrypt(text: str, key: bytes) -> bytes:
    fernet = Fernet(key)
    return fernet.encrypt(text.encode())


def decrypt(encrypted_data: bytes, key: bytes) -> int:
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_data).decode()


def save_snapshot(snapshot, password):
    text = f'{snapshot.gpa}-{snapshot.rank}-{snapshot. credits}-{snapshot.class_avg}-{snapshot.class_mid}' 
    key = generate_key(password)
    encrypted = encrypt(text, key)
    with open('./record.txt', 'wb+') as f:
        f.write(encrypted)


def read_snapshot(password):
    try:
        with open('./record.txt', 'rb') as f:
            text = f.readline()
            if text is None:
                return None
            key = generate_key(password)
            decrypted = decrypt(text, key)
            stats = decrypted.split('-')
            return Snapshot(float(stats[0]), float(stats[1]), float(stats[2]), float(stats[3]), float(stats[4]))
    except Exception:
        return None
            
        
if __name__ == '__main__':
    uid, psw, token = getenv("STD_ID"), getenv("PASSWORD"), getenv("TOKEN")
    assert (uid and psw and token)
    checker = GradeChecker(uid, psw)
    snapshot = checker.get_stat()
    checker.close()
    
    old_snapshot = read_snapshot(token)
    if snapshot.compare(old_snapshot):
        save_snapshot(snapshot, token)
        title = f'GPA {str(old_snapshot.gpa if old_snapshot is not None else 0.0)} -> {str(snapshot.gpa)}'
        url = f'http://www.pushplus.plus/send?token={token}&title={title}&content=排名：{int(old_snapshot.rank if old_snapshot is not None else 0.0)} -> {int(snapshot.rank)}&template=html'
        requests.get(url)
        print('update')
