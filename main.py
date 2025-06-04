# main.py — точка входа для TeleHerd GUI (PyQt5)

import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QPushButton, QVBoxLayout, QWidget, QLabel, QHBoxLayout, QMessageBox, QFrame
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect
from PyQt5.QtGui import QIcon, QPixmap

from core.account_manager import AccountManager
from core.proxy_manager import ProxyManager
from core.sms_manager import SMSManager
from core.messenger import Messenger
from core.responder import Responder

class TelegramFarmGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TeleHerd — Telegram Farm Manager")
        self.setGeometry(200, 150, 900, 600)
        self.setWindowIcon(QIcon("ui/teleherd.ico"))  # Добавьте свою иконку в ui/

        # Анимация плавного появления окна
        self.setWindowOpacity(0.0)
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(500)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.start()

        # Инициализация менеджеров
        self.account_manager = AccountManager()
        self.proxy_manager = ProxyManager()
        self.sms_manager = SMSManager()
        self.messenger = Messenger()
        self.responder = Responder()

        self.central_widget = QWidget()
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Красивая "шапка" с лого и тенью
        self.header_frame = QFrame(self)
        self.header_frame.setObjectName("HeaderFrame")
        self.header_frame.setFixedHeight(60)
        header_layout = QHBoxLayout(self.header_frame)
        header_layout.setContentsMargins(20, 0, 0, 0)

        # Лого: если файл есть, показываем, если нет — только текст
        try:
            pixmap = QPixmap("ui/teleherd_logo.png")
            if not pixmap.isNull():
                logo = QLabel()
                logo.setPixmap(pixmap.scaled(38, 38, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                header_layout.addWidget(logo)
        except Exception:
            pass

        self.label = QLabel("TeleHerd — Telegram Farm Manager", self)
        self.label.setObjectName("TitleLabel")
        header_layout.addWidget(self.label)
        header_layout.addStretch()
        self.layout.addWidget(self.header_frame)

        # Разделитель-тень под шапкой
        self.shadow_line = QFrame()
        self.shadow_line.setFrameShape(QFrame.HLine)
        self.shadow_line.setFrameShadow(QFrame.Sunken)
        self.shadow_line.setObjectName("ShadowLine")
        self.shadow_line.setFixedHeight(3)
        self.layout.addWidget(self.shadow_line)

        # Таблица аккаунтов
        self.table = QTableWidget(self)
        self.table.setStyleSheet("background-color: #1c1f26; alternate-background-color: #1c1f26; selection-background-color: #50577a; color: #e0e0e0")
        self.table.viewport().setStyleSheet("background-color: #1c1f26")
        self.table.setRowCount(0)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Прокси", "Статус", "Последнее действие"])
        self.table.viewport().setStyleSheet("background-color: #1c1f26")
        self.layout.addWidget(self.table)

        # Надпись “Нет аккаунтов”, если таблица пуста
        self.empty_label = QLabel("Нет аккаунтов — добавьте первый!")
        self.empty_label.setAlignment(Qt.AlignCenter)
        self.empty_label.setObjectName("EmptyLabel")
        self.layout.addWidget(self.empty_label)
        self.empty_label.hide()

        # Кнопки управления
        self.button_layout = QHBoxLayout()
        self.btn_register = QPushButton("Зарегистрировать аккаунт")
        self.btn_proxy = QPushButton("Назначить прокси")
        self.btn_broadcast = QPushButton("Запустить рассылку")
        self.btn_respond = QPushButton("Автоответчик")
        self.btn_refresh = QPushButton("Обновить список")

        for btn in [
            self.btn_register, self.btn_proxy, self.btn_broadcast, self.btn_respond, self.btn_refresh
        ]:
            self.button_layout.addWidget(btn)
        self.layout.addLayout(self.button_layout)

        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        # Стилизация (тёмная тема, округлые кнопки, плавные эффекты)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #23272f;
            }
            #HeaderFrame {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #323643, stop:1 #23272f
                );
                border-bottom: 2px solid #23272f;
                box-shadow: 0 4px 12px rgba(20,22,30,0.12);
            }
            #TitleLabel {
                color: #fff;
                font-size: 23px;
                font-weight: 800;
                letter-spacing: 1.5px;
                padding-left: 10px;
            }
            #ShadowLine {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 #23272f, stop:1 #444857
                );
            }
            QTableWidget {
                background-color: #1c1f26;
                color: #e0e0e0;
                border: 1px solid #444857;
                font-size: 16px;
                border-radius: 15px;
                gridline-color: #444857;
                selection-background-color: #3b3f53;
                selection-color: #fff;
            }
            QTableWidget, QTableWidget QTableCornerButton::section, QTableWidget::item {
                background-color: #1c1f26;
                color: #e0e0e0;
                border: none;
            }
            QHeaderView::section {
                background-color: #292d36;
                color: #ffffff;
                font-weight: bold;
                border-radius: 10px;
                padding: 8px;
            }
            QTableWidget QTableCornerButton::section {
                background: #292d36;
            }
            QTableWidget::item:selected {
                background: #50577a;
                color: #fff;
                transition: background 0.2s;
            }
            QPushButton {
                background-color: #383e4c;
                color: #fff;
                font-size: 15px;
                border-radius: 18px;
                padding: 10px 20px;
                margin: 6px;
                border: none;
                transition: background 0.2s;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #50577a;
            }
            QPushButton:pressed {
                background-color: #252832;
            }
            #EmptyLabel {
                color: #bbbbbb;
                font-size: 17px;
                font-style: italic;
                margin: 30px;
            }
        """)

        # Привязка кнопок к методам
        self.btn_register.clicked.connect(self.register_account)
        self.btn_proxy.clicked.connect(self.assign_proxy)
        self.btn_broadcast.clicked.connect(self.start_broadcast)
        self.btn_respond.clicked.connect(self.start_responder)
        self.btn_refresh.clicked.connect(self.load_accounts)

        # Инициализация/загрузка аккаунтов
        self.load_accounts()

    def load_accounts(self):
        accounts = self.account_manager.get_accounts()
        self.table.setRowCount(0)
        self.empty_label.hide()
        if not accounts:
            self.empty_label.show()
            return
        for acc in accounts:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(acc["id"])))
            self.table.setItem(row, 1, QTableWidgetItem(str(acc["proxy"])))
            self.table.setItem(row, 2, QTableWidgetItem(str(acc["status"])))
            self.table.setItem(row, 3, QTableWidgetItem(str(acc["last"])))

    def register_account(self):
        result = self.sms_manager.register_account()
        if result["success"]:
            self.account_manager.add_account(result["account"])
            QMessageBox.information(self, "Успех", f"Аккаунт {result['account']['id']} успешно зарегистрирован.")
            self.load_accounts()
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось зарегистрировать аккаунт.")

    def assign_proxy(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Ошибка", "Сначала выберите аккаунт в таблице.")
            return
        acc_id = self.table.item(selected, 0).text()
        proxy = self.proxy_manager.get_free_proxy()
        success = self.account_manager.assign_proxy(acc_id, proxy)
        if success:
            QMessageBox.information(self, "Готово", f"Прокси {proxy} назначен аккаунту {acc_id}.")
            self.load_accounts()
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось назначить прокси.")

    def start_broadcast(self):
        count = self.messenger.broadcast()
        QMessageBox.information(self, "Рассылка завершена", f"Сообщения разосланы ({count} чатов).")

    def start_responder(self):
        started = self.responder.start()
        if started:
            QMessageBox.information(self, "Автоответчик", "Автоответчик запущен.")
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось запустить автоответчик.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TelegramFarmGUI()
    window.show()
    sys.exit(app.exec_())
