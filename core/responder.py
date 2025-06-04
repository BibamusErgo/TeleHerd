# responder.py — автоответчик для TeleHerd

import os
from core.telegram_core import TelegramCore

TEMPLATES_PATH = os.path.join(os.path.dirname(__file__), '../messages/templates.txt')

class Responder:
    def __init__(self, account_manager=None):
        self.account_manager = account_manager  # для получения аккаунтов
        self.tg_core = TelegramCore()           # интеграция с Telethon
        self.templates = self._load_templates()
        self.running = False

    def _load_templates(self):
        if not os.path.exists(TEMPLATES_PATH):
            return ["Спасибо за ваш запрос!"]
        with open(TEMPLATES_PATH, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]

    def start(self):
        """
        Запускает автоответчик для всех аккаунтов. Заглушка для интеграции с Telethon.
        """
        self.running = True
        # Здесь будет цикл проверки входящих сообщений (polling через Telethon)
        # Пример: self.tg_core.listen_incoming_messages(callback=self._on_message)
        return True

    def stop(self):
        self.running = False

    def _on_message(self, account_id, from_user, text):
        """
        Колбек для обработки входящих сообщений. Здесь логика выбора и отправки ответа.
        """
        if not self.running:
            return
        reply = self.templates[0]  # Заглушка: всегда первый шаблон, можно сделать рандом
        # self.tg_core.send_message(account_id, from_user, reply)
