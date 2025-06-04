# messenger.py — рассылка сообщений для TeleHerd

import os
import random
from core.telegram_core import TelegramCore

TEMPLATES_PATH = os.path.join(os.path.dirname(__file__), '../messages/templates.txt')
CHATS_PATH = os.path.join(os.path.dirname(__file__), '../chats/chat_list.txt')

class Messenger:
    def __init__(self, account_manager=None):
        self.account_manager = account_manager  # для получения списка аккаунтов
        self.tg_core = TelegramCore()           # подключение к Telethon
        self.templates = self._load_templates()
        self.chats = self._load_chats()

    def _load_templates(self):
        if not os.path.exists(TEMPLATES_PATH):
            return ["Пример сообщения!"]
        with open(TEMPLATES_PATH, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]

    def _load_chats(self):
        if not os.path.exists(CHATS_PATH):
            return []
        with open(CHATS_PATH, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]

    def broadcast(self):
        """
        Рассылает случайное сообщение из шаблонов по всем чатам от всех (или выбранных) аккаунтов.
        Заглушка: требует интеграции с TelegramCore.
        """
        accounts = self.account_manager.get_accounts() if self.account_manager else []
        if not accounts:
            return 0
        count = 0
        for acc in accounts:
            for chat in self.chats:
                template = random.choice(self.templates)
                # self.tg_core.send_message(acc["id"], chat, template)  # интеграция позже
                count += 1
        return count
