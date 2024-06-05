import requests
import json
import psycopg2

def ConectaBD():
    with open('ConexaoBd.json') as j:
        credencial_bd = json.load(j)
    try:
        # Unpack the dictionary as keyword arguments
        conexao = psycopg2.connect(**credencial_bd)
        print('tudo ok')
        return conexao
    except psycopg2.OperationalError as e:
        print(e)
    return None


def BuscaListaIdsChamados():
    conexao = ConectaBD()
    cursor = conexao.cursor()
    query = """SELECT idchamado, statuscadastro FROM chamados WHERE date(datainsercao) = CURRENT_DATE;"""
    try:
        cursor.execute(query)
        lista_ids_chamados = cursor.fetchall()
        return lista_ids_chamados
    except psycopg2.OperationalError as e:
        print(e) 
    return None

def AtribuiChamaoAoTecnico(lista_ids_chamados):
    chamados_para_remover = []
    for item in lista_ids_chamados:
        id_chamado = item[0]
        status_cadastro = item[1]
        if status_cadastro == True:
            url = f"https://suporte.gavresorts.com.br/api/v3/requests/{id_chamado}/assign"
            headers = {"authtoken": "40605592-93B7-4820-B4E4-E352FA8A3754"}
            input_data = '''{
                "request": {
                    "technician": {
                        "name": "RPA"
                    }
                }
            }'''
        else:
            url = f"https://suporte.gavresorts.com.br/api/v3/requests/{id_chamado}/assign"
            headers = {"authtoken": "40605592-93B7-4820-B4E4-E352FA8A3754"}
            input_data = '''{
                "request": {
                    "technician": {
                        "name": "Ramirez Marques de Andrade Campello"
                    }
                }
            }'''
        data = {'input_data': input_data}
        response = requests.put(url, headers=headers, data=data, verify=False)
        print(response.text)
        # Adiciona o chamado à lista de chamados para remover se o status de cadastro não for True
        if status_cadastro != True:
            chamados_para_remover.append(item)
    
    # Remove os chamados da lista original
    for chamado in chamados_para_remover:
        lista_ids_chamados.remove(chamado)
    
    # Retorna a nova lista
    return lista_ids_chamados


def AlteraStatusChamado(lista_ids_chamados):
    lista_status = ['Atribuído', 'Em Progresso']    
    for item in lista_ids_chamados:
        id_chamado = item[0]
        url = f"https://suporte.gavresorts.com.br/api/v3/requests/{id_chamado}"
        headers = {"authtoken": "40605592-93B7-4820-B4E4-E352FA8A3754"}
        
        for status in lista_status:    
            input_data = f'''{{
                "request": {{
                    "status": {{
                        "name": "{status}"
                    }}
                }}
            }}'''
            data = {'input_data': input_data}
            response = requests.put(url, headers=headers, data=data, verify=False)
            print(response.text)

def EncaminhaResolucaoChamado(lista_ids_chamados):
    for item in lista_ids_chamados:
        id_chamado = item[0]
        url = f"https://suporte.gavresorts.com.br/api/v3/requests/{id_chamado}/resolutions"
        headers ={"authtoken":"40605592-93B7-4820-B4E4-E352FA8A3754"}
        input_data = '''{
            "resolution": {
                "content": "Colaborador cadastrado com sucesso."
            }
        }'''
        data = {'input_data': input_data}
        response = requests.post(url,headers=headers,data=data,verify=False)
        print(response.text)

def AdiconaLog(lista_ids_chamados):
    for item in lista_ids_chamados:
        id_chamado = item[0]     
        url = f"https://suporte.gavresorts.com.br/api/v3/requests/{id_chamado}/worklogs"
        headers ={"authtoken":"40605592-93B7-4820-B4E4-E352FA8A3754","accept" : "application/vnd.manageengine.sdp.v3+json"}
        input_data = '''{"worklog":{"owner":{"id":"7060","name":"RPA"}}}'''
        data = {'input_data': input_data}
        response = requests.post(url,headers=headers,data=data,verify=False)
        print(response.text)

def FechaChamado(lista_ids_chamados):
    lista_status = ['Resolução Proposta']   
    for item in lista_ids_chamados:
        id_chamado = item[0]
        url = f"https://suporte.gavresorts.com.br/api/v3/requests/{id_chamado}"
        headers = {"authtoken": "40605592-93B7-4820-B4E4-E352FA8A3754"}
        
        for status in lista_status:    
            input_data = f'''{{
                "request": {{
                    "status": {{
                        "name": "{status}"
                    }}
                }}
            }}'''
            data = {'input_data': input_data}
            response = requests.put(url = url, headers=headers, data=data, verify = False)
            print(response.text)

lista_ids_chamados = BuscaListaIdsChamados()

if lista_ids_chamados is None or len(lista_ids_chamados) == 0:
    print("Lista vazia")
    exit()

lista_ids_chamados_ = AtribuiChamaoAoTecnico(lista_ids_chamados)

AlteraStatusChamado(lista_ids_chamados)

EncaminhaResolucaoChamado(lista_ids_chamados)

AdiconaLog(lista_ids_chamados)

FechaChamado(lista_ids_chamados)
