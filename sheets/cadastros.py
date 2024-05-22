import gspread
from threading import Thread

gc = None

url = "https://docs.google.com/spreadsheets/d/1kXX6HRXpKvY8OOCfNPeZTgY4618dD3hdL9_8gWpXKvk/edit#gid=0"

def fazer_login():
    global gc
    print('(LOGIN) Acessando credenciais do Sheets')
    gc = gspread.service_account(filename="sheets/credentials.json")
    print('(LOGIN) Credenciais Aceitas')

def abrir_planilha():
    if gc is None:
        fazer_login()
    print('(ABERTURA) Abrindo URL da planilha')
    sheet = gc.open_by_url(url)
    print('(ABERTURA) URL Aberto e planilha importada!')
    return sheet

def cadastrar_sheets_zap(dados):
    sheet = abrir_planilha()
    worksheet = sheet.worksheet("PromPeriodicaWpp")
    dados_formatados = [[str(item) for item in dados]]
    worksheet.append_rows(dados_formatados)

    duplicados = worksheet.get_all_values()
    colunas = duplicados[0]
    dados_limpos = [list(item) for item in set(tuple(row) for row in duplicados)]
    dados_limpos.remove(colunas)
    worksheet.clear()
    worksheet.append_row(colunas)
    worksheet.append_rows(dados_limpos)

def cadastrar_sheets_tel(dados):
    sheet = abrir_planilha()
    worksheet = sheet.worksheet("PromPeriodicaTel")
    dados_formatados = [[str(item) for item in dados]]
    worksheet.append_rows(dados_formatados)

    duplicados = worksheet.get_all_values()
    colunas = duplicados[0]
    dados_limpos = [list(item) for item in set(tuple(row) for row in duplicados)]
    dados_limpos.remove(colunas)
    worksheet.clear()
    worksheet.append_row(colunas)
    worksheet.append_rows(dados_limpos)
