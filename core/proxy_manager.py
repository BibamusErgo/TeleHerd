# proxy_manager.py — работа с прокси через ProxyMarket API для TeleHerd

import requests
import os
import json

CONFIG_PATH = os.path.join(os.path.dirname(__file__), '../storage/config.json')

class ProxyManager:
    def __init__(self, config_path=CONFIG_PATH):
        self.config_path = config_path
        self.api_key = self._load_api_key()
        self.proxies = []
        self._load_proxies()

    def _load_api_key(self):
        # Ожидается, что config.json содержит { "proxy_market_api_key": "..." }
        if not os.path.exists(self.config_path):
            return None
        with open(self.config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config.get("proxy_market_api_key")

    def _load_proxies(self):
        # Можно хранить список купленных прокси в config.json, но лучше получать актуальный через API
        if not self.api_key:
            self.proxies = []
            return
        try:
            r = requests.get(
                'https://api.proxymarket.one/api/proxies',
                headers={"Authorization": self.api_key}
            )
            if r.status_code == 200:
                self.proxies = r.json().get('proxies', [])
            else:
                self.proxies = []
        except Exception:
            self.proxies = []

    def get_free_proxy(self):
        # Просто возвращаем первый свободный прокси из списка (можно доработать на учёт занятых)
        self._load_proxies()  # обновить список
        for proxy in self.proxies:
            # Допустим, что proxy — dict с ключами ip, port, login, password
            # Можно реализовать логику «свободен/занят»
            return f"{proxy['ip']}:{proxy['port']}"
        return None

    def mark_proxy_as_used(self, proxy_str):
        # В будущем: можно помечать прокси как занятый (например, добавить в config.json или отдельную БД)
        pass
