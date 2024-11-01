from telethon.sync import TelegramClient, events
import asyncio

# Замените 'YOUR_API_ID', 'YOUR_API_HASH' и 'YOUR_PHONE_NUMBER' на ваши данные.
api_id = 'до'
api_hash = 'угшу'
phone_number = '7'

# Создаем клиента Telethon.
client = TelegramClient(phone_number, api_id, api_hash)

# Словарь для хранения настроек каждого чата или личного сообщения.
chat_settings = {}

# Функция для отправки сообщения в чат или ЛС.
async def send_message(chat_id, delay_seconds, message_text):
    while chat_settings[chat_id]['sending_enabled']:
        await client.send_message(chat_id, message_text)
        await asyncio.sleep(delay_seconds)

# Обработка команды /start в чате или ЛС.
@client.on(events.NewMessage(pattern='/start (\d+)([\s\S]*)'))
async def start(event):
    chat_id = event.chat_id
    delay_seconds = int(event.pattern_match.group(1))
    message_text = event.pattern_match.group(2).strip()  # Убираем пробелы и переносы строк

    # Настройки для чата или ЛС
    chat_settings[chat_id] = {
        'sending_enabled': True,
        'delay_seconds': delay_seconds,
        'message_text': message_text
    }

    # Запуск задачи отправки сообщений
    asyncio.create_task(send_message(chat_id, delay_seconds, message_text))
    
    # Удаляем команду /start из чата или ЛС
    await event.delete()
    
    # Отправляем уведомление в "Избранное"
    me = await client.get_me()
    await client.send_message(me.id, f"Рассылка началась для {chat_id} с интервалом {delay_seconds} секунд.")

# Обработка команды /stop в чате или ЛС.
@client.on(events.NewMessage(pattern='/stop'))
async def stop(event):
    chat_id = event.chat_id
    if chat_id in chat_settings:
        chat_settings[chat_id]['sending_enabled'] = False

    # Удаляем команду /stop из чата или ЛС
    await event.delete()

    # Отправляем уведомление в "Избранное"
    me = await client.get_me()
    await client.send_message(me.id, f"Рассылка остановлена для {chat_id}.")

if __name__ == '__main__':
    with client:
        client.run_until_disconnected()
