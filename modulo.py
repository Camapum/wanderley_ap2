import requests
import pandas as pd
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ3OTE1ODMyLCJpYXQiOjE3NDUzMjM4MzIsImp0aSI6IjY3ZTRjOGIzYTM0NzQ5ZmM5N2UyMDYwNjI4ZWIyYzY2IiwidXNlcl9pZCI6Mjh9.wzkQiBk-U8aTs__Ra4jRUzAlxrI9LOZt4LrGYrxKUS8"
headers = {'Authorization': 'JWT {}'.format(token)}
params = {'ticker': 'AZZA','ano_tri': '20244T',}
r = requests.get('https://laboratoriodefinancas.com/api/v1/balanco',params=params, headers=headers)
dados = r.json()['dados'][0]
balanco = dados['balanco']
df_24 = pd.DataFrame(balanco)

import requests
import pandas as pd
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ3OTE1ODMyLCJpYXQiOjE3NDUzMjM4MzIsImp0aSI6IjY3ZTRjOGIzYTM0NzQ5ZmM5N2UyMDYwNjI4ZWIyYzY2IiwidXNlcl9pZCI6Mjh9.wzkQiBk-U8aTs__Ra4jRUzAlxrI9LOZt4LrGYrxKUS8"
headers = {'Authorization': 'JWT {}'.format(token)}
params = {'ticker': 'AZZA','ano_tri': '20234T',}
r = requests.get('https://laboratoriodefinancas.com/api/v1/balanco',params=params, headers=headers)
dados = r.json()['dados'][0]
balanco = dados['balanco']
df_23 = pd.DataFrame(balanco)

#FUNÇÃO PARA ACHAR O VALOR CONTABIL ATRAVÉS DA CONTA E DESCRIÇÃO 
def valor_contabil(df, conta, descricao):
    filtro_conta = df['conta'].str.contains(conta, case=False)
    filtro_descricao = df['descricao'].str.contains(descricao, case=False)
    valor = sum(df[filtro_conta & filtro_descricao]['valor'].values)
    return valor 

#FUNÇÃO PARA PEGAR O BALANÇO 
def pegar_balanco(ticker, ano_tri):
    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ3OTE1ODMyLCJpYXQiOjE3NDUzMjM4MzIsImp0aSI6IjY3ZTRjOGIzYTM0NzQ5ZmM5N2UyMDYwNjI4ZWIyYzY2IiwidXNlcl9pZCI6Mjh9.wzkQiBk-U8aTs__Ra4jRUzAlxrI9LOZt4LrGYrxKUS8'
    headers = {'Authorization': f'JWT {token}'}
    params = {'ticker': ticker, 'ano_tri': ano_tri}
    r = requests.get('https://laboratoriodefinancas.com/api/v1/balanco',params=params, headers=headers)
    dados = r.json()['dados'][0]
    balanco = dados['balanco']
    df = pd.DataFrame(balanco)
    return df

balanco_renner = pegar_balanco('LREN3', '20234T')
balanco_cea = pegar_balanco('CEAB3', '20234T')
balanco_guar = pegar_balanco('GUAR3', '20234T')
balanco_amar = pegar_balanco('AMAR3', '20234T')

#teste do modulo
print("Arquivo modulo.py carregado")
import sys
sys.path.append('c:\\Users\\juli6\\Documents\\ap2')



#TESTE DA CAPTAÇÃO DE DADOS DO BALANÇO 
# Lista de empresas e trimestres
empresas = ['LREN3', 'CEAB3', 'GUAR3', 'AMAR3']
trimestre_atual = '20234T'
trimestre_anterior = '20233T'

# Dicionário para armazenar os indicadores de cada empresa
indicadores_empresas = {}

# Obter os balanços e calcular os indicadores
for empresa in empresas:
    print(f"Processando indicadores para {empresa}...")
    try:
        # Obter os balanços para os dois trimestres
        df_24 = pegar_balanco(empresa, trimestre_atual)
        df_23 = pegar_balanco(empresa, trimestre_anterior)
        
        # Verificar se os DataFrames foram obtidos corretamente
        if df_24 is not None and df_23 is not None:
            # Calcular os indicadores
            indicadores = calcular_indicadores(df_24, df_23)
            # Armazenar os indicadores no dicionário
            indicadores_empresas[(empresa, trimestre_atual)] = indicadores
        else:
            print(f"⚠️ Não foi possível obter os balanços para {empresa}.")
    except Exception as e:
        print(f"Erro ao processar {empresa}: {e}")

# Função para obter os indicadores de uma empresa e trimestre
def obter_indicadores(empresa, ano_trimestre):
    chave = (empresa, ano_trimestre)
    if chave in indicadores_empresas:
        print(f"Indicadores para {empresa} no trimestre {ano_trimestre}:")
        for indicador, valor in indicadores_empresas[chave].items():
            print(f"  {indicador}: {valor}")
    else:
        print(f"⚠️ Indicadores para {empresa} no trimestre {ano_trimestre} não encontrados.")

# Exibir os indicadores calculados
for empresa in empresas:
    obter_indicadores(empresa, trimestre_atual)

#TESTE DO CALCULO DOS INDICADORES 
def calcular_indicadores(df_24, df_23):
    # Helper function to calculate accounting values
    def valor_contabil(df, conta, descricao):
        filtro_conta = df['conta'].str.contains(conta, case=False)
        filtro_descricao = df['descricao'].str.contains(descricao, case=False)
        valor = sum(df[filtro_conta & filtro_descricao]['valor'].values)
        return valor

    # Intangível, Imobilizado, Investimentos, e PL
    intangivel = valor_contabil(df_24, '^1.*', '^Intang*')
    imobilizado = valor_contabil(df_24, '^1.*', 'Imobilizados')
    investimentos = valor_contabil(df_24, '^1.*', 'Invest')
    pl = valor_contabil(df_24, '^2.*', 'patrim.nio')
    ipl = (intangivel + imobilizado + investimentos) / pl if pl else None

    # Estoque Médio
    estoque_24 = valor_contabil(df_24, '^1.01', 'estoque')
    estoque_23 = valor_contabil(df_23, '^1.01', 'estoque')
    estoque_medio = (estoque_24 + estoque_23) / 2

    # Indicadores de Liquidez
    ativo_circulante = valor_contabil(df_24, '^1.01', '')  # Ativo Circulante
    ativo_nao_circulante = valor_contabil(df_24, '^1.1', '')  # Ativo Não Circulante
    passivo_circulante = valor_contabil(df_24, '^2.01', '')  # Passivo Circulante
    passivo_nao_circulante = valor_contabil(df_24, '^2.02', '')  # Passivo Não Circulante
    disponibilidades = valor_contabil(df_24, '^1.01', 'Caixa|Bancos')  # Caixa e equivalentes
    estoques = valor_contabil(df_24, '^1.01', 'estoque')
    realizavel_curto_prazo = ativo_circulante - estoques - disponibilidades

    ccl = ativo_circulante - passivo_circulante  # Capital Circulante Líquido
    lc = ativo_circulante / passivo_circulante if passivo_circulante else None  # Liquidez Corrente
    ls = (ativo_circulante - estoques) / passivo_circulante if passivo_circulante else None  # Liquidez Seca
    li = disponibilidades / passivo_circulante if passivo_circulante else None  # Liquidez Imediata
    lg = (ativo_circulante + ativo_nao_circulante) / (passivo_circulante + passivo_nao_circulante)  # Liquidez Geral

    # Endividamento
    divida_total = passivo_circulante + passivo_nao_circulante
    endividamento_geral = divida_total / (ativo_circulante + ativo_nao_circulante)
    solvencia = (ativo_circulante + ativo_nao_circulante) / (passivo_circulante + passivo_nao_circulante)
    relacao_ct_cp = passivo_nao_circulante / passivo_circulante if passivo_circulante else None
    composicao_endividamento = passivo_circulante / divida_total if divida_total else None

    # Estoque e CMV
    cmv = valor_contabil(df_24, '^3.*', 'CMV')
    pme = 360 * (estoque_medio / cmv) if cmv else None
    ge = cmv / estoque_medio if estoque_medio else None

    # Prazo Médio
    receitas = valor_contabil(df_24, '^3.*', 'Receita')
    contas_receber = valor_contabil(df_24, '^1.01', 'Clientes|Duplicatas')
    pmr = 360 * contas_receber / receitas if receitas else None
    fornecedores = valor_contabil(df_24, '^2.01', 'Fornecedores')
    pmpf = 360 * fornecedores / cmv if cmv else None

    # Ciclos
    co = pme + pmr if pme is not None and pmr is not None else None
    cf = co - pmpf if co is not None and pmpf is not None else None
    ce = 360 / ge if ge else None

    # Capital de Giro
    ncg = ativo_circulante - fornecedores - contas_receber - estoques
    st = ccl - ncg  # Saldo em Tesouraria
    cg = ativo_circulante - passivo_circulante

    # Return all indicators as a dictionary
    return {
        "ipl": ipl,
        "estoque_medio": estoque_medio,
        "ccl": ccl,
        "lc": lc,
        "ls": ls,
        "li": li,
        "lg": lg,
        "endividamento_geral": endividamento_geral,
        "solvencia": solvencia,
        "relacao_ct_cp": relacao_ct_cp,
        "composicao_endividamento": composicao_endividamento,
        "pme": pme,
        "ge": ge,
        "pmr": pmr,
        "pmpf": pmpf,
        "co": co,
        "cf": cf,
        "ce": ce,
        "ncg": ncg,
        "st": st,
        "cg": cg
    }

for empresa, indicadores in indicadores_empresas.items():
    print(f"\nIndicadores para {empresa}:")
    print(f"Trimestre {trimestre_atual}:")
    for indicador, valor in indicadores.items():
        print(f"  {indicador}: {valor}")

# Função para obter os indicadores de uma empresa e trimestre
def obter_indicadores(empresa, ano_trimestre):
    # Verificar se os indicadores já foram calculados
    chave = (empresa, ano_trimestre)
    if chave in indicadores_empresas:
        print(f"Indicadores para {empresa} no trimestre {ano_trimestre}:")
        for indicador, valor in indicadores_empresas[chave].items():
            print(f"  {indicador}: {valor}")
    else:
        print(f"⚠️ Indicadores para {empresa} no trimestre {ano_trimestre} não encontrados.")

# Exibir os indicadores calculados
obter_indicadores('LREN3', '20234T')
obter_indicadores('CEAB3', '20234T')
obter_indicadores('GUAR3', '20234T')
obter_indicadores('AMAR3', '20234T')


def indicador_comparacao(df):
    lucro = valor_contabil(df, '^3.*', 'Lucro')
    pl = valor_contabil(df, '^2.*', 'patrim.nio')
    roe = (lucro / pl) * 100 if pl else None
    capital_oneroso = (valor_contabil(df, '^2.*', '^empr.*')+valor_contabil(df, '^2.*', '^deb.*'))
    investimento = capital_oneroso + pl
    wi = capital_oneroso
    eva = (lucro - wi) * 100 / investimento if investimento else None
    return {
        'roe': roe,
        'eva': eva
    }

# #comparativo back test (1,5,10 anos) a partir do eva e roe
# #pegar os periodos de "23-04-01" a "24-03-31" (1ano)
# #comparar com o ibov no mesmo periodo

# def main():
#     list_tickers = ['LREN3', 'CEAB3', 'GUAR3', 'AMAR3']
#     list_tri = ["20243T"]
#     df_comparacao = pd.DataFrame()
#     for ticker in list_tickers:
#         for trimestre in list_tri:
#             # ticker = "EZTC3"
#             # trimestre = "20234T"
#             df = pegar_balanco(ticker, trimestre)
#             comparacao = indicador_comparacao(df)
#             df_final = pd.DataFrame()
#             df_final["ticker"]=[ticker]
#             df_final["roe"]=comparacao["roe"]
#             df_final["eva"]=comparacao["eva"]
#             df_comparacao = pd.concat([df_comparacao, df_final], axis=0,ignore_index=True)
#         print(df_comparacao)

# main()

import requests
import pandas as pd
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ5OTA0Mjc4LCJpYXQiOjE3NDczMTIyNzgsImp0aSI6IjgzZTMxZGFhNzI4NzRlMWE4NWY2N2I3YzJjYzMzZDZjIiwidXNlcl9pZCI6NjZ9.ZtM6X8drdxAFJaO8weGa_IH3Ii64WWHRN2PSomQ8X7g"
headers = {'Authorization': 'JWT {}'.format(token)}

def pegar_preco_corrigido(ticker, data_inicial, data_final):
    params = {
        'ticker': ticker,
        'data_inicial': data_inicial,
        'data_final': data_final
    }
    r = requests.get('https://laboratoriodefinancas.com/api/v1/preco-corrigido', params=params, headers=headers)
    dados = r.json()['dados']
    return pd.DataFrame(dados)

def pegar_preco_diversos(ticker, data_inicial, data_final):
    params = {
        'ticker': ticker,
        'data_inicial': data_inicial,
        'data_final': data_final
    }
    r = requests.get('https://laboratoriodefinancas.com/api/v1/preco-diversos', params=params, headers=headers)
    dados = r.json()['dados']
    return pd.DataFrame(dados)
