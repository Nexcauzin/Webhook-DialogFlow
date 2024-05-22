import httpx
import telegram.error
from telegram import Bot
import schedule
import pandas as pd
from sheets import ler_telegram
from sheets.cadastros import fazer_login
from threading import Thread
import time

token_telegram = '7047287612:AAEMimLtSeFAbVsgkY8cmGKnZZhVjon5vik'

def send_telegram_message():
    ler_telegram.ConfereListaTelegram()
    dados_telegram = pd.read_json('cron/dados_telegram.json')
    tentas = 0

    while tentas < len(dados_telegram):
        try:
            bot = Bot(token=token_telegram)
            user_id = int(dados_telegram['ID'][tentas])

            with open('cron/MensagemTelegram.txt', 'r+', encoding='utf-8') as file:
                message = file.read()

            bot.send_message(chat_id=user_id, text=message, parse_mode='Markdown')
            tentas += 1

        except (telegram.error.NetworkError, httpx.ConnectError) as erro:
            print(f'Erro:{erro} | Iteração:{tentas}')
            continue

def schedule_messages():
    fazer_login()  # Faz login apenas aqui uma vez
    schedule.every(15).days.do(lambda: Thread(target=send_telegram_message).start())

    while True:
        schedule.run_pending()
        time.sleep(60)

def main():
    schedule_messages()
