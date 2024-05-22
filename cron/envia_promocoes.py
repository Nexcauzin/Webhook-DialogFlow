import asyncio
import httpx
import telegram.error
from telegram import Bot
import schedule
import pandas as pd
from sheets import ler_telegram
from sheets.cadastros import fazer_login


token_telegram = '7047287612:AAEMimLtSeFAbVsgkY8cmGKnZZhVjon5vik'

#id meu: 2079298675
#id de jf: 6758080824

def send_telegram_message():
    ler_telegram.ConfereListaTelegram()
    ler_telegram.ConfereListaTelegram() # Pegando os dados atualizados
    dados_telegram = pd.read_json('cron/dados_telegram.json') #Salvando em um DataFrame
    tentas = 0 #Variável que vai ser iterada

    while tentas < len(dados_telegram):
        try:
            bot = Bot(token = token_telegram)
            user_id = int(dados_telegram['ID'][tentas])

            # Leitura do texto que será enviado
            with open('cron/MensagemTelegram.txt', 'r+', encoding='utf-8') as file:
                message = file.read()

            # Envio da mensagem
            bot.send_message(chat_id=user_id, text=message, parse_mode='Markdown')

            tentas += 1 # Para iterar no loop

        except(telegram.error.NetworkError, httpx.ConnectError) as erro:
            print(f'Erro:{erro} | Iteração:{tentas}')
            continue

# Executando a função de forma assíncrona
#asyncio.run(send_telegram_message())

def main():
    fazer_login()
    ## Abaixo a lógica do Cron
    # schedule.every(2).minutes.do(lambda: )
    while True:
        asyncio.sleep(60)
        schedule.run_pending()

