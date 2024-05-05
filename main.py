__author__='nexcauzin'

from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Pra salvar as variáveis e armazenar no banco
dados_cont_plan = []
dados_cad_prom = []

# Importando os Custom Payload:
with open('custom_payloads/contratar_plano.json', 'r+', encoding='utf-8') as cont_plan:
    contratar_plano = json.load(cont_plan)

with open('custom_payloads/cadastro_promocoes.json', 'r+', encoding='utf-8') as cad_num:
    cadastro_promocoes = json.load(cad_num)

with open('custom_payloads/promocoes_ativas.json', 'r+', encoding='utf-8') as ver_prom:
    ver_promocoes = json.load(ver_prom)

@app.route('/', methods=['POST'])
def main():
    data = request.get_json(silent=True)

    contextos = data['queryResult']['outputContexts']

    # Depois arrumar uma lógica para contexto geral, só ir pegando os parâmetros para se basear na ação
    # Bloco 1 -> Testa se é para Contratar Plano
    try:
        for contexto in contextos:
            parametros = contexto['parameters']
            plano = parametros['Plano']
            nome = parametros['person']['name']
            empresa = parametros['nome_empresa']
            dados_cont_plan.append({'plano': plano,
                                    'nome': nome,
                                    'empresa': empresa})
            print(f'Plano: {plano} | nome: {nome} | empresa: {empresa}')


        if data['originalDetectIntentRequest']['source'] == 'telegram':
            data['fulfillmentText'] = [{"payload": contratar_plano}]
        # elif data['originalDetectIntentRequest']['source'] == 'whatsapp':

    except:
        pass


    # Bloco 2 -> Testa se é para Cadastrar na Lista de Transmissão
    try:
        for contexto in contextos:
            parametros = contexto['parameters']
            nome = parametros['person']['name']
            numero = parametros['phone-number']
            dados_cad_prom.append({'nome': nome,
                                   'numero': numero})
            print(f'Nome: {nome} | Tel: {numero}')

        if data['originalDetectIntentRequest']['source'] == 'telegram':
            data['fulfillmentText'] = [{"payload": cadastro_promocoes}]
        # elif data['originalDetectIntentRequest']['source'] == 'whatsapp':

    except:
        pass


    # Bloco 3 -> Testa se é para ver Promoções Ativas
    # Depois melhora para um Webhook que puxa a mensagem de algum lugar automaticamente
    try:
        for contexto in contextos:
            parametros = contexto['parameters']
            # Teste de existência para o parametro promoções
            promocoes = parametros['Promocoes']

        if data['originalDetectIntentRequest']['source'] == 'telegram':
            data['fulfillmentText'] = [{"payload": ver_promocoes}]


    except:
        pass

    # Descomenta quando quiser o json bruto
    #print(data)


    return jsonify(data)

if __name__ == "__main__":
    app.debug = False
    app.run()