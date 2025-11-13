import os
import qrcode
from io import BytesIO
from PIL import Image
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Токен бота - укажите ваш токен от @BotFather
BOT_TOKEN = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка команды /start"""
    await update.message.reply_text(
        'Привет! Отправь мне текст или ссылку, и я создам для тебя QR-код.'
    )

async def generate_qr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Генерация QR-кода из текста или ссылки"""
    user_message = update.message.text

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(user_message)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    img_buffer = BytesIO()
    img.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    await update.message.reply_photo(
        photo=img_buffer,
        caption=f'QR-код для: {user_message}'
    )

def main():
    """Запуск бота"""
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_qr))

    application.run_polling()

if __name__ == '__main__':
    main()
