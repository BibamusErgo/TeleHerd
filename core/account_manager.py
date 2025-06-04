# account_manager.py — управление аккаунтами TeleHerd

import os
import sqlite3
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), '../storage/accounts.db')

class AccountManager:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Создаёт таблицу, если её нет"""
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS accounts (
                id TEXT PRIMARY KEY,
                proxy TEXT,
                status TEXT,
                last TEXT
            )''')
            conn.commit()

    def get_accounts(self):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("SELECT id, proxy, status, last FROM accounts")
            rows = c.fetchall()
        accounts = [
            {"id": row[0], "proxy": row[1], "status": row[2], "last": row[3]} for row in rows
        ]
        return accounts

    def add_account(self, account):
        # account: dict с ключами id, proxy, status, last
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("INSERT OR REPLACE INTO accounts (id, proxy, status, last) VALUES (?, ?, ?, ?)",
                      (account["id"], account["proxy"], account["status"], account["last"]))
            conn.commit()

    def remove_account(self, account_id):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("DELETE FROM accounts WHERE id=?", (account_id,))
            conn.commit()

    def assign_proxy(self, account_id, proxy):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("UPDATE accounts SET proxy=?, last=? WHERE id=?", (proxy, datetime.now().strftime('%d.%m.%Y %H:%M'), account_id))
            conn.commit()
            # Проверим, что изменилось (1 — успех)
            return c.rowcount == 1

    def update_status(self, account_id, status):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("UPDATE accounts SET status=?, last=? WHERE id=?", (status, datetime.now().strftime('%d.%m.%Y %H:%M'), account_id))
            conn.commit()
            return c.rowcount == 1
