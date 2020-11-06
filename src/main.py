from .auth import Auth
from .store import Store


class ZhiXueBot:
    store: Store

    auth: Auth

    def __init__(self):
        self.store = Store()
        self.auth = Auth(self.store)

    def run(self):
        self.auth.login()
