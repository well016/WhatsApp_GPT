import random
import requests
from datetime import datetime
from json import dumps
import json
from whatsapp_api_client_python import API
import config
import re

greenAPI = API.GreenAPI(config.ID_WHATSAPP, config.TOKEN_WHATSAPP)

# Список URL изображений для случайного выбора
with open("good_morning.json", "r") as file:
    image_urls = json.load(file)




# URL для отправки файлов
api_url = "https://1103.api.green-api.com"
id_instance = config.ID_WHATSAPP
api_token_instance = config.TOKEN_WHATSAPP

# Формирование правильного URL
url = f"{api_url}/waInstance{id_instance}/sendFileByUrl/{api_token_instance}"



def main():
    # Запуск получения уведомлений
    greenAPI.webhooks.startReceivingNotifications(handler)


def handler(type_webhook: str, body: dict) -> None:
    if type_webhook == "incomingMessageReceived":
        incoming_message_received(body)
    elif type_webhook == "outgoingMessageReceived":
        outgoing_message_received(body)
    elif type_webhook == "outgoingAPIMessageReceived":
        outgoing_api_message_received(body)
    elif type_webhook == "outgoingMessageStatus":
        outgoing_message_status(body)
    elif type_webhook == "stateInstanceChanged":
        state_instance_changed(body)
    elif type_webhook == "deviceInfo":
        device_info(body)
    elif type_webhook == "incomingCall":
        incoming_call(body)
    elif type_webhook == "statusInstanceChanged":
        status_instance_changed(body)


def get_notification_time(timestamp: int) -> str:
    return str(datetime.fromtimestamp(timestamp))


def incoming_message_received(body: dict) -> None:
    """Обработка входящего сообщения"""
    timestamp = body.get("timestamp")
    time = get_notification_time(timestamp)

    # Получение данных отправителя
    sender = body["senderData"]["chatId"]
    sender_name = body["senderData"]["senderName"]

    # Попытка извлечь текстовое сообщение
    message_data = body.get("messageData", {})
    message_type = message_data.get("typeMessage", "")

    # Обрабатываем текстовое сообщение
    if message_type == "textMessage":
        message_text = message_data.get("textMessageData", {}).get("textMessage", "Нет текста")
        clean_message = re.sub(r"[^\w\s]", "", message_text.lower())
        # Проверяем, если сообщение содержит "доброе утро"
        if "доброе утро" in clean_message or 'хәерле иртә' in clean_message:
            # Выбираем случайное изображение
            image_url = random.choice(image_urls)
            file_name = "image.png"  # Можно задать любое имя файла

            # Отправляем изображение
            send_image(sender, image_url, file_name, "Доброе утро!")

        else:
            # Логика для обработки других сообщений
            # reply_text = f"Вы написали: {message_text}"
            # send_message(sender, reply_text)
            pass


def send_message(chat_id: str, text: str) -> None:
    """Функция отправки сообщения"""
    response = greenAPI.sending.sendMessage(chat_id, text)
    if response.code == 200:
        print(f"Сообщение '{text}' успешно отправлено в чат {chat_id}.")
    else:
        print(f"Ошибка при отправке сообщения в чат {chat_id}: {response.error}")


def send_image(chat_id: str, image_url: str, file_name: str, caption: str) -> None:
    """Функция отправки изображения"""
    payload = {
        "chatId": chat_id,
        "urlFile": image_url,
        "fileName": file_name,
        "caption": caption
    }

    headers = {
        'Content-Type': 'application/json'
    }

    # Отправляем запрос на сервер для отправки изображения
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        print(f"Изображение '{file_name}' успешно отправлено в чат {chat_id}.")
    else:
        print(f"Ошибка при отправке изображения в чат {chat_id}: {response.text}")


def outgoing_message_received(body: dict) -> None:
    timestamp = body["timestamp"]
    time = get_notification_time(timestamp)

    data = dumps(body, ensure_ascii=False, indent=4)
    print(f"New outgoing message at {time} with data: {data}", end="\n\n")


def outgoing_api_message_received(body: dict) -> None:
    timestamp = body["timestamp"]
    time = get_notification_time(timestamp)

    data = dumps(body, ensure_ascii=False, indent=4)
    print(f"New outgoing API message at {time} with data: {data}", end="\n\n")


def outgoing_message_status(body: dict) -> None:
    timestamp = body["timestamp"]
    time = get_notification_time(timestamp)

    data = dumps(body, ensure_ascii=False, indent=4)
    print(f"Status of sent message has been updated at {time} with data: {data}", end="\n\n")


def state_instance_changed(body: dict) -> None:
    timestamp = body["timestamp"]
    time = get_notification_time(timestamp)

    data = dumps(body, ensure_ascii=False, indent=4)
    print(f"Current instance state at {time} with data: {data}", end="\n\n")


def device_info(body: dict) -> None:
    timestamp = body["timestamp"]
    time = get_notification_time(timestamp)

    data = dumps(body, ensure_ascii=False, indent=4)
    print(f"Current device information at {time} with data: {data}", end="\n\n")


def incoming_call(body: dict) -> None:
    timestamp = body["timestamp"]
    time = get_notification_time(timestamp)

    data = dumps(body, ensure_ascii=False, indent=4)
    print(f"New incoming call at {time} with data: {data}", end="\n\n")


def status_instance_changed(body: dict) -> None:
    timestamp = body["timestamp"]
    time = get_notification_time(timestamp)

    data = dumps(body, ensure_ascii=False, indent=4)
    print(f"Current instance status at {time} with data: {data}", end="\n\n")


if __name__ == '__main__':
    main()
