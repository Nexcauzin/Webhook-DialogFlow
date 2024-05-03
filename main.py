__author__='nexcauzin'

from flask import Flask, request, jsonify

app = Flask(__name__)

contrata_plano = []

@app.route('/', methods=['POST'])
def main():
    data = request.get_json(silent=True)

    if 'outputContexts' in data['queryResult']:
        contextos = data['queryResult']['outputContexts']

        # Depois arrumar uma lógica para contexto geral, só ir pegando os parâmetros para se basear na ação
        for contexto in contextos:
            if 'planos-followup' in contexto['name']:
                parametros = contexto['parameters']
                plano = parametros['Plano']
                nome = parametros['person']['name']
                empresa = parametros['nome_empresa']

        #print(data)
        print(f'Plano: {plano} | nome: {nome} | empresa: {empresa}')
        data['fulfillmentText'] = f'Tudo certo! {nome}, seus dados foram salvos, em breve, em horário comercial, um atendente irá falar com você e dar prosseguimento a contratação do seu plano!\n\nNós agradecemos o seu contato e a sua preferência!😉'

    else:
        print('JSON incompatível')

    return jsonify(data)

# run Flask app
if __name__ == "__main__":
    app.debug = False
    app.run()