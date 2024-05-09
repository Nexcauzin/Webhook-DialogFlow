import pandas as pd
import gspread
from threading import Thread

gc = None

url = "https://docs.google.com/spreadsheets/d/1kXX6HRXpKvY8OOCfNPeZTgY4618dD3hdL9_8gWpXKvk/edit#gid=0"

def fazer_login():
    global gc
    # Acessando as credenciais
    print('(LOGIN) Acessando credenciais do Sheets')
    gc = gspread.service_account(filename="sheets/credentials.json")
    print('(LOGIN) Credenciais Aceitas')

def abrir_planilha():
    if gc is None:
        fazer_login()
    # Abrindo a URL da planilha
    print('(ABERTURA) Abrindo URL da planilha')
    sheet = gc.open_by_url(url)
    print('(ABERTURA) URL Aberto e planilha importada!')
    return sheet

def cadastrar_sheets(dados):
    # Abrindo planilha
    sheet = abrir_planilha()

    worksheet = sheet.worksheet("PromPeriodica")
    dados_formatados = [[str(item) for item in dados]]
    worksheet.append_rows(dados_formatados)


    ## ESSE TRATAMENTO SÓ TA FUNCIONANDO PARA DUPLICADOS DE NOME E TELEFONE
    # Pensar num tratamento para quando tiver duplicado de Telefone
    #(pode ser até na hora de mandar as mensagens periodicas)
    # Tratando os duplicados:
    duplicados = worksheet.get_all_values()
    colunas = ['Nome', 'Telefone'] # Pegando os nomes das colunas, só por garantia (teve uma época que tava duplicando todos os dados ;-;)
    dados_limpos = [list(item) for item in set(tuple(row) for row in duplicados)] # Tirando duplicados
    dados_limpos.remove(colunas)
    worksheet.clear() # Limpando sheet
    worksheet.append_row(colunas) # Linha de nomes do Sheet
    worksheet.append_rows(dados_limpos) # Linhas de dados


def cadastro_assinc(dados):
    thread = Thread(target=cadastrar_sheets, args=(dados,))
    thread.start()


def confere_lista():
    # Abrindo planilha
    sheet = abrir_planilha()
    print('(AGENDAMENTO) URL Aberto e planilha importada!')
    worksheet = sheet.worksheet("PromPeriodica")

    #for i in range(1, len(worksheet)):
        #Aqui a lógica para iterar a cada item do worksheet enviando a mensagem!