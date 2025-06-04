# telegram_core.py — взаимодействие с Telethon для TeleHerd

from telethon import TelegramClient, events
import os

SESSIONS_DIR = os.path.join(os.path.dirname(__file__), '../storage/sessions')
API_ID = None   # будет загружаться из config.json
API_HASH = None # будет загружаться из config.json

class TelegramCore:
    def __init__(self, api_id=API_ID, api_hash=API_HASH):
        self.api_id = api_id
        self.api_hash = api_hash
        # Здесь можно хранить {account_id: TelegramClient()}
        self.clients = {}
        # TODO: загрузка api_id и api_hash из config.json, если не передано

    def get_client(self, account_id, session_path=None, proxy=None):
        """
        Возвращает (или создаёт) TelegramClient для аккаунта.
        session_path — путь к .session файлу; proxy — данные прокси
        """
        if account_id in self.clients:
            return self.clients[account_id]
        # Путь к .session файлу:
        if not session_path:
            session_path = os.path.join(SESSIONS_DIR, f"{account_id}.session")
        client = TelegramClient(session_path, self.api_id, self.api_hash, proxy=proxy)
        self.clients[account_id] = client
        return client

    def send_message(self, account_id, chat, text):
        """
        Отправляет сообщение в чат/пользователю от имени аккаунта.
        """
        client = self.get_client(account_id)
        async def _send():
            await client.start()
            await client.send_message(chat, text)
            await client.disconnect()
        import asyncio
        asyncio.run(_send())

    def listen_incoming_messages(self, account_id, callback):
        """
        Слушает входящие сообщения для аккаунта и вызывает callback(account_id, from_user, text)
        """
        client = self.get_client(account_id)
        @client.on(events.NewMessage(incoming=True))
        async def handler(event):
            sender = await event.get_sender()
            from_user = sender.username or sender.id
            text = event.raw_text
            callback(account_id, from_user, text)
        async def _run():
            await client.start()
            await client.run_until_disconnected()
        import asyncio
        asyncio.run(_run())
