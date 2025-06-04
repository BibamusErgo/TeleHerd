# TeleHerd

TeleHerd is an experimental desktop application for managing multiple Telegram accounts. It uses **PyQt5** for the GUI and **Telethon** for interacting with Telegram.

## Features

- Simple account storage using SQLite
- Integration placeholders for SMS activation and proxy management
- Graphical interface with account table and basic actions

Most features are currently stubs and require further development.

## Requirements

- Python 3.10+
- See `requirements.txt` for required packages

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Run the GUI application:

```bash
python main.py
```

Configuration such as API keys is stored in `storage/config.json`. Do **not** commit your real credentials to version control.

## License

This project is released under the MIT License.
