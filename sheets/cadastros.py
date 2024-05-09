import pandas as pd
import gspread
from threading import Thread

def cadastrar_sheets(dados):
    # Acessando as credenciais
    print('Acessando credenciais do Sheets')
    gc = gspread.service_account(filename="credentials.json")

    print('Credenciais Aceitas')
    # Abrindo a URL
    print('Abrindo URL da planilha')
    sheet = gc.open_by_url("https://docs.google.com/spreadsheets/d/1kXX6HRXpKvY8OOCfNPeZTgY4618dD3hdL9_8gWpXKvk/edit#gid=0")
    print('URL Aberto e planilha importada!')
    worksheet = sheet.worksheet("PromPeriodica")
    worksheet.append_rows(dados)


def cadastro_assinc(dados):
    thread = Thread(target=cadastrar_sheets, args=(dados,))
    thread.start()

def confere_lista():
    # Acessando as credenciais
    print('(AGENDAMENTO) Acessando credenciais do Sheets')
    gc = gspread.service_account(filename="credentials.json")

    print('(AGENDAMENTO) Credenciais Aceitas')
    # Abrindo a URL
    print('(AGENDAMENTO) Abrindo URL da planilha')
    sheet = gc.open_by_url(
        "https://docs.google.com/spreadsheets/d/1kXX6HRXpKvY8OOCfNPeZTgY4618dD3hdL9_8gWpXKvk/edit#gid=0")
    print('(AGENDAMENTO) URL Aberto e planilha importada!')
    worksheet = sheet.worksheet("PromPeriodica")

    #for i in range(1, len(worksheet)):
        #Aqui a lógica para iterar a cada item do worksheet enviando a mensagem!
