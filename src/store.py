import pickle
from pathlib import Path
from typing import Optional, AnyStr

from appdirs import user_data_dir
from requests.cookies import RequestsCookieJar


class Store:
    dir: Path

    def __init__(self):
        self.dir = Path(user_data_dir("zhixue-bot", "JingBh"))
        if not self.dir.exists():
            self.dir.mkdir(parents=True)

    @property
    def cookies(self) -> Optional[RequestsCookieJar]:
        file = self.dir / "cookies"
        if file.exists():
            with open(file, "rb") as handler:
                return pickle.load(handler)

    @cookies.setter
    def cookies(self, value: RequestsCookieJar):
        file = self.dir / "cookies"
        with open(file, "wb") as handler:
            pickle.dump(value, handler)

    @staticmethod
    def get_asset(filename: str, encoding: str = None) -> Optional[AnyStr]:
        this_file = Path(__file__).absolute()
        assets_dir = this_file.parent / "assets"
        file = assets_dir / filename
        if file.exists():
            if encoding:
                handler = file.open("r", encoding=encoding)
            else:
                handler = file.open("rb")
            return handler.read()
        else:
            return None
