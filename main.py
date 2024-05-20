__author__='nexcauzin'

from flask import Flask, request, jsonify
from sheets import cadastros
from cron import envia_promocoes
from sheets.cadastros import fazer_login, cadastrar_sheets_zap, cadastrar_sheets_tel
from cron.envia_promocoes import main

app = Flask(__name__)

# Variáveis para o envio periódico de mensagens:
# TOKEN do bot Telegram
envia_promocoes.token_telegram = '7047287612:AAEMimLtSeFAbVsgkY8cmGKnZZhVjon5vik'

# Pra iniciar já com login
cadastros.asyncio.run(fazer_login())

# Inicializandao o CRON
envia_promocoes.asyncio.run(main())

@app.route('/', methods=['POST'])
def main():
    data = request.get_json(silent=True, force=True)

    contextos = data['queryResult']['outputContexts']

    # Bloco 1 -> Testa se é para Cadastrar na Lista de Transmissão (WhatsApp
    try:
        for contexto in contextos:
            parametros = contexto['parameters']
            nome = parametros['nome']
            numero = parametros['numero']
            #dados_cad_prom.append([nome, numero])
            print(f'Nome: {nome} | Tel: {numero}')
            # Realiza o cadastro assíncrono com Threads
            cadastros.asyncio.run(cadastrar_sheets_zap([nome, numero]))

    except:
        pass


        # Bloco 2 -> Testa se é para Cadastrar na Lista de Transmissão (Telegram)
    try:
        for contexto in contextos:
            parametros = contexto['parameters']
            nome = parametros['nome']
            id = data['session'].split('/')[-1]
            # dados_cad_prom.append([nome, numero])
            print(f'Nome: {nome} | ID: {id}')
            # Realiza o cadastro assíncrono com Threads
            cadastros.asyncio.run(cadastrar_sheets_tel([nome, id]))

    except:
        pass


    # Descomenta quando quiser o json bruto
    print(data)

    return jsonify(data)


if __name__ == "__main__":
    app.debug = False
    app.run()