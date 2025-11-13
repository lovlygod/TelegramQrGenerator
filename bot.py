import os
import qrcode
from io import BytesIO
from PIL import Image, ImageDraw
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Токен бота - укажите ваш токен от @BotFather
BOT_TOKEN = os.getenv('BOT_TOKEN', '8085337425:AAFB4-QWzQItMjjgpiLLj71-Lm5XDI0GLPw')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'Привет! Отправь мне текст или ссылку, и я создам для тебя QR-код.'
    )

async def generate_qr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    
    # Извлекаем параметры из сообщения
    args = context.args if context.args else []
    logo_path = None
    fill_color = "black"
    back_color = "white"
    
    # Парсим аргументы
    for arg in args:
        if arg.startswith('logo:'):
            logo_path = arg[5:]  # Убираем 'logo:' из начала
        elif arg.startswith('color:'):
            colors = arg[6:].split(',')
            if len(colors) >= 2:
                fill_color = colors[0]
                back_color = colors[1]
    
    # Создаем QR-код
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(user_message)
    qr.make(fit=True)

    # Создаем изображение QR-кода с заданными цветами
    qr_img = qr.make_image(fill_color=fill_color, back_color=back_color)
    qr_img = qr_img.convert('RGB')
    
    # Добавляем логотип, если указан
    if logo_path and os.path.exists(logo_path):
        # Открываем изображение логотипа
        logo = Image.open(logo_path)
        
        # Определяем размеры QR-кода
        qr_width, qr_height = qr_img.size
        
        # Рассчитываем размер логотипа (1/4 от размера QR-кода)
        logo_size = min(qr_width, qr_height) // 4
        
        # Изменяем размер логотипа
        logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
        
        # Вычисляем позицию для центрирования логотипа
        logo_pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
        
        # Вставляем логотип в центр QR-кода
        qr_img.paste(logo, logo_pos)
    
    # Сохраняем изображение в байтовый поток
    img_buffer = BytesIO()
    qr_img.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    await update.message.reply_photo(
        photo=img_buffer,
        caption=f'QR-код для: {user_message}'
    )

def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("qr", generate_qr))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_qr))

    application.run_polling()

if __name__ == '__main__':
    main()
