__author__ = 'nexcauzin'

from flask import Flask, request, jsonify
from sheets import cadastros
from cron import envia_promocoes
from sheets.cadastros import cadastrar_sheets_zap, cadastrar_sheets_tel
from threading import Thread

app = Flask(__name__)

# Variáveis para o envio periódico de mensagens:
# TOKEN do bot Telegram
envia_promocoes.token_telegram = '7047287612:AAEMimLtSeFAbVsgkY8cmGKnZZhVjon5vik'

# Inicializando o CRON
def start_cron():
    cron_thread = Thread(target=envia_promocoes.main)
    cron_thread.start()

start_cron()

@app.route('/', methods=['POST'])
def main_route():
    data = request.get_json(silent=True, force=True)
    contextos = data['queryResult']['outputContexts']

    # Bloco 1 -> Testa se é para Cadastrar na Lista de Transmissão (WhatsApp)
    try:
        for contexto in contextos:
            parametros = contexto['parameters']
            nome = parametros['nome']
            numero = parametros['numero']
            print(f'Nome: {nome} | Tel: {numero}')
            Thread(target=cadastrar_sheets_zap, args=([nome, numero],)).start()
    except Exception as e:
        print(f"Erro no cadastro do WhatsApp: {e}")

    # Bloco 2 -> Testa se é para Cadastrar na Lista de Transmissão (Telegram)
    try:
        for contexto in contextos:
            parametros = contexto['parameters']
            nome = parametros['nome']
            id = data['session'].split('/')[-1]
            print(f'Nome: {nome} | ID: {id}')
            Thread(target=cadastrar_sheets_tel, args=([nome, id],)).start()
    except Exception as e:
        print(f"Erro no cadastro do Telegram: {e}")

    # Descomenta quando quiser o json bruto
    #print(data)

    return jsonify(data)


if __name__ == "__main__":
    app.debug = False
    app.run()
