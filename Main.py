import json;
import requests;
import psycopg2;
import logging;

def Conecta_ao_banco():
    try:
        conexao = psycopg2.connect(
            host='generalizado',
            port='generalizado',
            user='generalizado',
            password='generalizado',
            dbname='generalizado'
        )
    except psycopg2.OperationalError as e:
        logging.error(f'O erro {e} ocorreu ao tentar conectar ao banco de dados.')
        print(e)
    return conexao

def Buscar_chamados():
    lista_chamados = []
    conexao = Conecta_ao_banco()
    cursor = conexao.cursor()
    comando = "SELECT idchamado, statuscadastro FROM chamados WHERE date(datainsercao) = CURRENT_DATE;"
    try:
        cursor.execute(comando)
        tupla_chamados = cursor.fetchall()
        for dados in tupla_chamados:
            lista_chamados.append([dados[0], dados[1]])
        return lista_chamados
    except psycopg2.OperationalError as e:
        logging.error(f'O erro {e} ocorreu ao tentar executar o comando SQL.')
        print(e)
        return None

def Atribui_chamado(lista_chamados):
    lista_chamados_atualizada = []
    for chamados in lista_chamados:
        if chamados[1] == True:
            url = f'https://suporte.gavresorts.com.br/api/v3/requests/{chamados[0]}/assign'
            headers = {"authtoken": "Inhackeavel"}
            input_data = '''{
                            "request": {
                                "technician": {
                                    "name": "RPA"
                                }
                            }
                        }'''
        else:
            url = f'https://suporte.gavresorts.com.br/api/v3/requests/{chamados[0]}/assign'
            headers = {"authtoken": "Inhackeavel"}
            input_data = '''{
                            "request": {
                                "technician": {
                                    "name": "Ramirez Marques de Andrade Campello"
                                }
                            }
                        }'''
        data = {'input_data': input_data}
        response = requests.put(url, headers = headers, data = data, verify = False)
        print(response.status_code)
    for chamados in lista_chamados:
        if (chamados[1] == True):
            lista_chamados_atualizada.append(chamados)
    return lista_chamados_atualizada

def Altera_status_chamado(lista_chamados):
    status_chamado = ['Atribuído', 'Em Progresso']
    for chamados in lista_chamados:
        url = f'https://suporte.gavresorts.com.br/api/v3/requests/{chamados[0]}'
        headers = {"authtoken": "Inhackeavel"}
        for status in status_chamado:
            input_data = f'''{{
                "request": {{
                    "status": {{
                        "name": "{status}"
                    }}
                }}
            }}'''
            data = {'input_data': input_data}
            response = requests.put(url = url, headers = headers,data = data, verify = False)
            print(response.status_code)
    
def Encaminha_resolucao_chamado(lista_chamados):
    for chamados in lista_chamados:
        url = f'https://suporte.gavresorts.com.br/api/v3/requests/{chamados[0]}/resolutions'
        headers = {"authtoken": "Inhackeavel"}
        input_data = '''{
                    "resolution": {
                        "content": "Colaborador cadastrado com sucesso."
                    }
                }'''
        data = {'input_data': input_data}
        response = requests.post(url = url, headers = headers, data = data, verify = False)
        print(response.status_code)

def AdiconaLog(lista_chamados):
    for chamados in lista_chamados:
        url = f'https://suporte.gavresorts.com.br/api/v3/requests/{chamados[0]}/worklogs'
        headers ={"authtoken": "Inhackeavel"}
        input_data = '''{"worklog":{"owner":{"id":"7060","name":"RPA"}}}'''
        data = {'input_data': input_data}
        response = requests.post(url = url,headers = headers,data = data,verify = False)
        print(response.status_code)

def Fecha_chamado(lista_chamados):
    lista_status = ['Resolução Proposta']
    for chamado in lista_chamados:
        url = f'https://suporte.gavresorts.com.br/api/v3/requests/{chamado[0]}'
        headers = {"authtoken": "Inhackeavel"}
        for status in lista_status:
            input_data = f'''{{
                "request": {{
                    "status": {{
                        "name": "{status}"
                    }}
                }}
            }}'''
            data = {'input_data': input_data}
            response = requests.put(url = url, headers = headers, data = data, verify = False)
            print(response.status_code)



#Main():
lista_chamados = Buscar_chamados
if (lista_chamados == None):
    print("Lista está vazia")
    exit()
lista_chamados = Atribui_chamado(lista_chamados)
Altera_status_chamado(lista_chamados)
Encaminha_resolucao_chamado(lista_chamados)
AdiconaLog(lista_chamados)
Fecha_chamado(lista_chamados)
