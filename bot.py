import os
import logging
import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

load_dotenv()

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Путь к вашему JSON файлу с ключами Google API
GOOGLE_CREDENTIALS_FILE = 'path_to_your_credentials.json'

# ID вашей Google таблицы
SPREADSHEET_ID = os.getenv("GOOGLE_SPREADSHEET_ID")

# Функция для подключения к Google Sheets
def get_google_sheet():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_CREDENTIALS_FILE, scope)
    client = gspread.authorize(credentials)
    sheet = client.open_by_key(SPREADSHEET_ID).sheet1
    return sheet

# Функция для очистки и форматирования номера телефона
def format_phone_number(phone_input: str) -> str:
    # Удаляем все символы, кроме цифр
    digits = re.sub(r'[^0-9]', '', phone_input)

    # Заменяем "00" (международный код доступа) на "+"
    if digits.startswith('00'):
        digits = '+' + digits[2:]

    # Если номер начинается с "8" и имеет длину 11 цифр, заменяем "8" на "+7"
    if digits.startswith('8') and len(digits) == 11:
        digits = '+7' + digits[1:]

    # Если номер не начинается с "+", добавляем его
    if not digits.startswith('+'):
        digits = '+' + digits

    # Проверяем длину номера (например, от 7 до 15 цифр)
    if len(digits) < 7 or len(digits) > 15:
        return ''

    return digits

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Привет! Пожалуйста, отправьте мне свой номер телефона.')

# Обработка текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_input = update.message.text.strip()

    # Очищаем и форматируем номер телефона
    formatted_phone = format_phone_number(user_input)

    if not formatted_phone:
        await update.message.reply_text('Пожалуйста, введите корректный номер телефона.')
        return

    sheet = get_google_sheet()
    phone_numbers = sheet.col_values(1)  # Предполагаем, что номера телефонов хранятся в первом столбце

    if formatted_phone in phone_numbers:
        await update.message.reply_text('Данный номер уже присутствует в таблице.')
    else:
        sheet.append_row([formatted_phone])
        await update.message.reply_text(f'Ваш номер успешно добавлен в таблицу: {formatted_phone}')

# Обработка ошибок
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main() -> None:
    # Токен вашего бота
    BOT_TOKEN =  os.getenv("BOT_TOKEN")

    # Создаем приложение и передаем ему токен бота
    application = Application.builder().token(BOT_TOKEN).build()

    # Регистрируем обработчики команд
    application.add_handler(CommandHandler("start", start))

    # Регистрируем обработчик текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Регистрируем обработчик ошибок
    application.add_error_handler(error)

    # Запускаем бота
    application.run_polling()

if __name__ == '__main__':
    main()