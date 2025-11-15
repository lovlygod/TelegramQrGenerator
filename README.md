<div align="center">
  <h1 style="margin-top: 24px;">💎 Telegram QR Generator by @lovlydev</h1>

  <p style="font-size: 18px; margin-bottom: 24px;">
    <b>Telegram-бот для генерации QR-кодов</b>
  </p>

[Report Bug](https://github.com/lovlygod/TelegramQrGenerator/issues) · [Request Feature](https://github.com/lovlygod/TelegramQrGenerator/issues)

</div>

---

## ✨ Features

- 🖼️ **QR Code Generation** - Generate QR codes from text or links
- 🤖 **Automatic Message Processing** - Automatically process text messages
- 📤 **Image Sending** - Send QR codes as images with captions
- 🎨 **Logo Integration** - Add logos to the center of QR codes
- 🌈 **Color Schemes** - Support for various QR code color schemes

## 🚀 Quick Start

### 1. Installation

```bash
git clone https://github.com/lovlygod/TelegramQrGenerator.git
cd TelegramQrGenerator
pip install -r requirements.txt
```

### 2. Configuration

Replace `YOUR_BOT_TOKEN` in `bot.py` file with your bot token from [@BotFather](https://t.me/BotFather):

```python
bot = telegram.Bot(token='YOUR_BOT_TOKEN')
```

### 3. Usage

Run the bot:

```bash
python bot.py
```

## Commands and Features

After starting the bot:

1. Send `/start` command to begin
2. Send any text message - the bot will generate a QR code for this text

### Advanced Features:

- To add a logo to the QR code: `/qr Text for QR code logo:path/to/image.png`
- To change colors: `/qr Text for QR code color:red,white` (line color, background color)

## Requirements

- Python >= 3.8
- Libraries: python-telegram-bot, qrcode[pil]

## License
[MIT](LICENSE)

<div align="center">

### Made with ❤️ by [@lovly](https://t.me/lovlyswag)

**Star ⭐ this repo if you found it useful!**

</div>
