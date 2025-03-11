from typing import Dict


class CookieHeaderStore:
    _instances: Dict[str, "CookieHeaderStore"] = {}

    def __new__(cls, name: str):
        if name not in cls._instances:
            cls._instances[name] = super(CookieHeaderStore, cls).__new__(cls)
            cls._instances[name].headers = {}
            cls._instances[name].cookies = {}
        return cls._instances[name]
