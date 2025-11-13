import os
import qrcode
import math
from io import BytesIO
from PIL import Image, ImageDraw
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Предустановленные цветовые схемы
COLOR_SCHEMES = {
    'neon': ('#FF00FF', '#00FFFF'),  # фуксия и бирюзовый
    'pastel': ('#FFB3BA', '#BAFFC9'),  # пастельно-розовый и пастельно-зеленый
    'dark_theme': ('#FFD700', '#2F2F2F'),  # золотой и темно-серый
    'ocean': ('#077BE', '#20B2AA'),  # синий и морская волна
    'sunset': ('#FF4E50', '#F9D423'),  # красный и желтый
    'forest': ('#4A5D23', '#8A9A5B'),  # темно-зеленый и светло-зеленый
    'lava': ('#FF4136', '#FF851B'),  # красный и оранжевый
    'ice': ('#7FDBFF', '#0074D9'),  # голубой и синий
    'cherry': ('#FF6B6B', '#FFD166'),  # вишня и бежевый
    'mint': ('#95E1D3', '#A8E6CF')   # мятный и светло-зеленый
}

# Токен бота - укажите ваш токен от @BotFather
BOT_TOKEN = os.getenv('BOT_TOKEN', '8085337425:AAFB4-QWzQItMjjgpiLLj71-Lm5XDI0GLPw')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'Привет! Отправь мне текст или ссылку, и я создам для тебя QR-код.' \
        ' Используй /help для получения дополнительной информации.' \
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "🤖 <b>Помощь по использованию бота QR-кодов</b>\n\n"
        "<b>Основные команды:</b>\n"
        "/start - Приветственное сообщение\n"
        "/help - Это сообщение помощи\n"
        "/qr <i>[текст]</i> - Создать QR-код с указанным текстом\n\n"
        
        "<b>Дополнительные возможности:</b>\n"
        "• <code>/qr текст color:цвет1,цвет2</code> - QR-код с заданными цветами\n"
        "• <code>/qr текст color:neon</code> - QR-код с предустановленной схемой\n"
        "• <code>/qr текст scheme:pastel</code> - QR-код с предустановленной схемой\n"
        "• <code>/qr текст gradient</code> - QR-код с градиентной заливкой\n\n"
        
        "<b>Поддерживаемые цветовые схемы:</b>\n"
        "• neon, pastel, dark_theme, ocean\n"
        "• sunset, forest, lava, ice, cherry, mint\n\n"
        
        "<b>Примеры использования:</b>\n"
        "<code>/qr Привет, мир!</code>\n"
        "<code>/qr https://example.com color:red,white</code>\n"
        "<code>/qr Мой сайт color:neon gradient</code>"
    )
    await update.message.reply_text(help_text, parse_mode='HTML')

async def generate_qr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Извлекаем текст из команды
    if context.args:
        user_message = ' '.join(context.args)
    else:
        user_message = update.message.text
        # Убираем команду из сообщения
        if user_message.startswith('/qr'):
            user_message = user_message[4:].strip()
    
    # Убираем команду из сообщения, если это обычное сообщение
    if update.message.text.startswith('/qr'):
        user_message = ' '.join(update.message.text.split(' ')[1:])
    
    # Извлекаем параметры из сообщения
    fill_color = "black"
    back_color = "white"
    color_scheme = None
    
    # Парсим аргументы из сообщения
    message_parts = user_message.split()
    filtered_message_parts = []
    
    for part in message_parts:
        if part.startswith('color:'):
            colors = part[6:].split(',')
            if len(colors) >= 2:
                # Проверяем, является ли это предустановленной схемой
                if colors[0] in COLOR_SCHEMES:
                    fill_color, back_color = COLOR_SCHEMES[colors[0]]
                else:
                    # Проверяем формат HEX
                    fill_color = colors[0] if colors[0].startswith('#') else colors[0]
                    back_color = colors[1] if colors[1].startswith('#') else colors[1]
        elif part.startswith('scheme:'):
            scheme_name = part[7:]  # Убираем 'scheme:' из начала
            if scheme_name in COLOR_SCHEMES:
                fill_color, back_color = COLOR_SCHEMES[scheme_name]
        elif part == 'gradient':
            # Отмечаем, что нужно применить градиент
            pass  # градиент будет применен позже
        else:
            filtered_message_parts.append(part)
    
    # Обновляем user_message, убирая служебные параметры
    user_message = ' '.join(filtered_message_parts)
    
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
    
    # Если запрошена градиентная заливка
    if 'gradient' in user_message.split():
        qr_img = apply_gradient_fill(qr_img, fill_color, back_color)
    
    
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
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("qr", generate_qr))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_qr))

    application.run_polling()

def hex_to_rgb(value):
    """Конвертирует HEX цвет в RGB"""
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def apply_gradient_fill(image, color1, color2):
    """Применяет градиентную заливку к изображению QR-кода"""
    width, height = image.size
    pixels = image.load()
    
    # Конвертируем цвета в RGB
    if color1.startswith('#'):
        color1 = hex_to_rgb(color1)
    else:
        # Для простых названий цветов используем предопределенные значения
        color_map = {
            'black': (0, 0, 0),
            'white': (255, 255, 255),
            'red': (255, 0, 0),
            'green': (0, 128, 0),
            'blue': (0, 0, 255),
            'yellow': (255, 255, 0),
            'cyan': (0, 255, 255),
            'magenta': (255, 0, 255),
            'orange': (255, 165, 0),
            'purple': (128, 0, 128),
            'pink': (255, 192, 203)
        }
        color1 = color_map.get(color1.lower(), (0, 0, 0))
    
    if color2.startswith('#'):
        color2 = hex_to_rgb(color2)
    else:
        color_map = {
            'black': (0, 0, 0),
            'white': (255, 255, 255),
            'red': (255, 0, 0),
            'green': (0, 128, 0),
            'blue': (0, 0, 255),
            'yellow': (255, 255, 0),
            'cyan': (0, 255, 255),
            'magenta': (255, 0, 255),
            'orange': (255, 165, 0),
            'purple': (128, 0, 128),
            'pink': (255, 192, 203)
        }
        color2 = color_map.get(color2.lower(), (255, 255, 255))
    
    # Создаем градиент
    for y in range(height):
        # Вычисляем соотношение для градиента (от 0 до 1)
        ratio = y / height
        
        # Интерполируем цвета
        r = int(color1[0] + (color2[0] - color1[0]) * ratio)
        g = int(color1[1] + (color2[1] - color1[1]) * ratio)
        b = int(color1[2] + (color2[2] - color1[2]) * ratio)
        gradient_color = (r, g, b)
        
        # Меняем цвет только для белых пикселей (фона)
        for x in range(width):
            r, g, b = pixels[x, y]
            # Если пиксель был белым (фон), применяем градиент
            if (r, g, b) == (255, 255, 255):
                pixels[x, y] = gradient_color
    
    return image

if __name__ == '__main__':
    main()
