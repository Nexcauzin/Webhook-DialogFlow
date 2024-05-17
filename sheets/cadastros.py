import gspread
import asyncio

gc = None

url = "https://docs.google.com/spreadsheets/d/1kXX6HRXpKvY8OOCfNPeZTgY4618dD3hdL9_8gWpXKvk/edit#gid=0"

async def fazer_login():
    global gc
    # Acessando as credenciais
    print('(LOGIN) Acessando credenciais do Sheets')
    gc = gspread.service_account(filename="sheets/credentials.json")
    print('(LOGIN) Credenciais Aceitas')

async def abrir_planilha():
    if gc is None:
        await fazer_login()
    # Abrindo a URL da planilha
    print('(ABERTURA) Abrindo URL da planilha')
    sheet = gc.open_by_url(url)
    print('(ABERTURA) URL Aberto e planilha importada!')
    return sheet

async def cadastrar_sheets(dados):
    # Abrindo planilha
    sheet = await abrir_planilha()

    worksheet = sheet.worksheet("PromPeriodicaWpp")
    dados_formatados = [[str(item) for item in dados]]
    worksheet.append_rows(dados_formatados)


    ## ESSE TRATAMENTO SÓ TA FUNCIONANDO PARA DUPLICADOS DE NOME E TELEFONE
    # Pensar num tratamento para quando tiver duplicado de Telefone
    #(pode ser até na hora de mandar as mensagens periodicas)
    # Tratando os duplicados:
    duplicados = worksheet.get_all_values()
    #print(duplicados[0])
    colunas = duplicados[0] # Pegando os nomes das colunas, só por garantia (teve uma época que tava duplicando todos os dados ;-;)
    dados_limpos = [list(item) for item in set(tuple(row) for row in duplicados)] # Tirando duplicados
    dados_limpos.remove(colunas)
    worksheet.clear() # Limpando sheet
    worksheet.append_row(colunas) # Linha de nomes do Sheet
    worksheet.append_rows(dados_limpos) # Linhas de dados

