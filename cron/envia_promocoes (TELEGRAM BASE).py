import asyncio

import httpx
import telegram.error
from telegram import Bot

#token = '6315254600:AAE0XXGHcfV2TsVsbTL-FECvihTKXvNF800'
token = '7047287612:AAEMimLtSeFAbVsgkY8cmGKnZZhVjon5vik'
id_usuario = '2079298675'

#id meu: 2079298675
#id de jf: 6758080824

async def send_telegram_message():
    try:
        bot = Bot(token=token)
        user_id = id_usuario

        # Leitura do texto que será enviado
        with open('MensagemTelegram.txt', 'r+', encoding='utf-8') as file:
            message = file.read()

        # Envio da mensagem
        await bot.send_message(chat_id=user_id, text=message, parse_mode='Markdown')

    except(telegram.error.NetworkError, httpx.ConnectError) as erro:
        print(f'Erro de conexão: {erro}')


# Executando a função de forma assíncrona
asyncio.run(send_telegram_message())
