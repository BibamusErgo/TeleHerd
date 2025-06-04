# sms_manager.py — регистрация Telegram-аккаунтов через SMS-Activate для TeleHerd

import requests
import os
import json
from datetime import datetime

CONFIG_PATH = os.path.join(os.path.dirname(__file__), '../storage/config.json')

class SMSManager:
    def __init__(self, config_path=CONFIG_PATH):
        self.config_path = config_path
        self.api_key = self._load_api_key()

    def _load_api_key(self):
        # Ожидается, что config.json содержит { "sms_activate_api_key": "..." }
        if not os.path.exists(self.config_path):
            return None
        with open(self.config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config.get("sms_activate_api_key")

    def buy_number(self):
        # Покупка номера для регистрации Telegram через SMS-Activate API
        if not self.api_key:
            return {"success": False, "error": "API-ключ SMS-Activate не задан"}
        params = {
            "api_key": self.api_key,
            "service": "tg",
            "country": "0",  # 0 — любая страна, можно добавить выбор страны
        }
        try:
            r = requests.get("https://api.sms-activate.org/stubs/handler_api.php", params={
                "api_key": self.api_key,
                "action": "getNumber",
                "service": "tg",
                "country": 0,
            })
            if 'ACCESS_NUMBER' in r.text:
                parts = r.text.strip().split(':')
                return {"success": True, "id": parts[1], "number": parts[2]}
            else:
                return {"success": False, "error": r.text}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def set_status(self, id, status):
        # Устанавливает статус (6 — готово, 8 — отмена, 3 — SMS получена)
        try:
            r = requests.get("https://api.sms-activate.org/stubs/handler_api.php", params={
                "api_key": self.api_key,
                "action": "setStatus",
                "id": id,
                "status": status,
            })
            return r.text
        except Exception as e:
            return str(e)

    def get_sms(self, id):
        # Получение кода из SMS
        try:
            r = requests.get("https://api.sms-activate.org/stubs/handler_api.php", params={
                "api_key": self.api_key,
                "action": "getStatus",
                "id": id,
            })
            if 'STATUS_OK' in r.text:
                parts = r.text.strip().split(':')
                return parts[1]  # код подтверждения
            else:
                return None
        except Exception:
            return None

    def register_account(self):
        """
        Полная процедура регистрации Telegram-аккаунта (эмуляция, требует Telethon для передачи кода)
        Здесь только заготовка! В рабочем коде будет интеграция с telegram_core.
        """
        result = self.buy_number()
        if not result["success"]:
            return {"success": False, "error": result["error"]}
        # Дальнейшая логика: через Telethon отправить запрос на регистрацию, принять код, завершить регистрацию
        # ...
        # После успеха:
        # self.set_status(result["id"], 6)
        # return {"success": True, "account": {"id": phone, ...}}
        return {"success": False, "error": "Заглушка. Интеграция с Telethon будет позже."}
