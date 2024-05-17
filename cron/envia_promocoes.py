import asyncio

import httpx
import telegram.error
from telegram import Bot
import schedule
import time
import pandas as pd
from sheets import ler_telegram

token_telegram = '7047287612:AAEMimLtSeFAbVsgkY8cmGKnZZhVjon5vik'
#token_telegram = None
id_usuario = '2079298675'

#id meu: 2079298675
#id de jf: 6758080824

async def send_telegram_message():
    ler_telegram.ConfereListaTelegram() # Pegando os dados atualizados
    dados_telegram = pd.read_json('dados_telegram.json') #Salvando em um DataFrame
    tentas = 0 #Variável que vai ser iterada

    while tentas < len(dados_telegram):
        try:
            bot = Bot(token = token_telegram)
            user_id = int(dados_telegram['ID'][tentas])

            # Leitura do texto que será enviado
            with open('MensagemTelegram.txt', 'r+', encoding='utf-8') as file:
                message = file.read()

            # Envio da mensagem
            await bot.send_message(chat_id=user_id, text=message, parse_mode='Markdown')

            tentas += 1 # Para iterar no loop

        except(telegram.error.NetworkError, httpx.ConnectError) as erro:
            print(f'Erro:{erro} | Iteração:{tentas}')
            continue

# Executando a função de forma assíncrona
#asyncio.run(send_telegram_message())

async def main():

    schedule.every(5).seconds.do(lambda: asyncio.create_task(send_telegram_message()))
    while True:
        await asyncio.sleep(1)
        schedule.run_pending()

asyncio.run(main())