import pandas as pd
from sheets import cadastros

def ConfereListaTelegram():
    # Abrindo planilha
    sheet = cadastros.abrir_planilha()
    print('(TELEGRAM) URL Aberto e planilha importada!')
    worksheet = sheet.worksheet("PromPeriodicaTel")
    # Pegando os valores
    dados = worksheet.get_all_values()
    colunas = dados.pop(0)

    # Colocando em um DF
    infos_telegram = pd.DataFrame(data=dados, columns=colunas)
    print(infos_telegram)
    infos_telegram.to_json('cron/dados_telegram.json', orient='records')
