from requestium import Session
from selenium.webdriver.support.expected_conditions import url_matches
from selenium.webdriver.support.wait import WebDriverWait
from requests import Request

from .store import Store

BASE_DOMAIN = "zhixue.com"
BASE_URL = f"https://www.{BASE_DOMAIN}"
LOGIN_URL = f"{BASE_URL}/login.html"
LOGIN_SUCCESS_PATTERN = rf"^{BASE_URL}/container/container/student/index"


def token_auth(r: Request) -> Request:
    from uuid import uuid1 as guid
    from time import time
    from hashlib import md5
    authguid = str(guid())
    timestamp = str(round(time() * 1000))
    password = "iflytek!@#123student"
    origin = authguid + timestamp + password
    token = md5(origin.encode()).hexdigest()
    r.headers["authbizcode"] = "0001"
    r.headers["authguid"] = authguid
    r.headers["authtimestamp"] = timestamp
    r.headers["authtoken"] = token
    return r


class Auth:
    store: Store

    session: Session

    token: str = "null"

    def __init__(self, store: Store = None):
        self.store = store if store else Store()
        self.session = Session("chromedriver", "chrome", webdriver_options={
            "arguments": [f"app={BASE_URL}"]
        })
        if cookies := self.store.cookies:
            self.session.cookies = cookies

    def login(self):
        while self.token == "null":
            if new_token := self.get_token():
                self.token = new_token
            else:
                self._try_login()

    def get_token(self) -> str:
        url = f"{BASE_URL}/addon/error/book/index"
        response = self.session.get(url, auth=token_auth, headers={
            "XToken": "null"
        })
        data = response.json()
        if "result" in data and data["result"]:
            return data["result"]

    def _try_login(self):
        browser = self.session.driver
        browser.get(LOGIN_URL)
        # browser.execute_script(Store.get_asset("login.js", "utf-8"))
        wait = WebDriverWait(browser, 180)
        wait.until(url_matches(LOGIN_SUCCESS_PATTERN))
        self.session.transfer_driver_cookies_to_session()
        self.store.cookies = self.session.cookies
