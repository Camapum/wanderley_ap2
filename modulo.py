import requests
import pandas as pd
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUwOTM0ODEyLCJpYXQiOjE3NDgzNDI3ODQsImp0aSI6IjEwODkzOTVmZWUxODRhNDJhNGU0NDc1MGM3ZDAwMjFmIiwidXNlcl9pZCI6NjZ9.LIlgZXw3GMaSzx-aBSQC50cJSZDn0UVk-zc1bZJotHE"
headers = {'Authorization': 'JWT {}'.format(token)}
params = {'ticker': 'AZZA','ano_tri': '20244T',}
r = requests.get('https://laboratoriodefinancas.com/api/v1/balanco',params=params, headers=headers)
dados = r.json()['dados'][0]
balanco = dados['balanco']
df_24 = pd.DataFrame(balanco)

import requests
import pandas as pd
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUwOTM0ODEyLCJpYXQiOjE3NDgzNDI3ODQsImp0aSI6IjEwODkzOTVmZWUxODRhNDJhNGU0NDc1MGM3ZDAwMjFmIiwidXNlcl9pZCI6NjZ9.LIlgZXw3GMaSzx-aBSQC50cJSZDn0UVk-zc1bZJotHE"
headers = {'Authorization': 'JWT {}'.format(token)}
params = {'ticker': 'AZZA','ano_tri': '20234T',}
r = requests.get('https://laboratoriodefinancas.com/api/v1/balanco',params=params, headers=headers)
dados = r.json()['dados'][0]
balanco = dados['balanco']
df_23 = pd.DataFrame(balanco)


#FUNÇÃO PARA PEGAR O BALANÇO 
def pegar_balanco(ticker, ano_tri):
    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUwOTM0ODEyLCJpYXQiOjE3NDgzNDI3ODQsImp0aSI6IjEwODkzOTVmZWUxODRhNDJhNGU0NDc1MGM3ZDAwMjFmIiwidXNlcl9pZCI6NjZ9.LIlgZXw3GMaSzx-aBSQC50cJSZDn0UVk-zc1bZJotHE'
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

print(balanco_renner)
print(balanco_cea)
print(balanco_guar)
print(balanco_amar)

#teste valor_contabil 
def valor_contabil(df, conta, descricao):
    filtro_conta = df['conta'].str.contains(conta, case=False, na=False)
    filtro_descricao = df['descricao'].str.contains(descricao, case=False, na=False)
    return df.loc[filtro_conta & filtro_descricao, 'valor'].sum()

#teste indicadores 
def calcular_indicadores(df_24, df_23):
    intangivel = valor_contabil(df_24, '^1.*', '^Intang*')
    imobilizado = valor_contabil(df_24, '^1.*', 'Imobilizados')
    investimentos = valor_contabil(df_24, '^1.*', 'Invest')
    pl = valor_contabil(df_24, '^2.*', 'patrim.nio')
    ipl = (intangivel + imobilizado + investimentos) / pl if pl else None

    estoque_24 = valor_contabil(df_24, '^1.01', 'estoque')
    estoque_23 = valor_contabil(df_23, '^1.01', 'estoque')
    estoque_medio = (estoque_24 + estoque_23) / 2

    ativo_circulante = valor_contabil(df_24, '^1.01', '')
    ativo_nao_circulante = valor_contabil(df_24, '^1.1', '')
    passivo_circulante = valor_contabil(df_24, '^2.01', '')
    passivo_nao_circulante = valor_contabil(df_24, '^2.02', '')
    disponibilidades = valor_contabil(df_24, '^1.01', 'Caixa|Bancos')
    estoques = valor_contabil(df_24, '^1.01', 'estoque')

    ccl = ativo_circulante - passivo_circulante
    lc = ativo_circulante / passivo_circulante if passivo_circulante else None
    ls = (ativo_circulante - estoques) / passivo_circulante if passivo_circulante else None
    li = disponibilidades / passivo_circulante if passivo_circulante else None
    lg = (ativo_circulante + ativo_nao_circulante) / (passivo_circulante + passivo_nao_circulante) if (passivo_circulante + passivo_nao_circulante) else None

    divida_total = passivo_circulante + passivo_nao_circulante
    endividamento_geral = divida_total / (ativo_circulante + ativo_nao_circulante) if (ativo_circulante + ativo_nao_circulante) else None
    solvencia = (ativo_circulante + ativo_nao_circulante) / (passivo_circulante + passivo_nao_circulante) if (passivo_circulante + passivo_nao_circulante) else None
    relacao_ct_cp = passivo_nao_circulante / passivo_circulante if passivo_circulante else None
    composicao_endividamento = passivo_circulante / divida_total if divida_total else None

    cmv = valor_contabil(df_24, '^3.*', 'CMV')
    pme = 360 * (estoque_medio / cmv) if cmv else None
    ge = cmv / estoque_medio if estoque_medio else None

    receitas = valor_contabil(df_24, '^3.*', 'Receita')
    contas_receber = valor_contabil(df_24, '^1.01', 'Clientes|Duplicatas')
    pmr = 360 * contas_receber / receitas if receitas else None
    fornecedores = valor_contabil(df_24, '^2.01', 'Fornecedores')
    pmpf = 360 * fornecedores / cmv if cmv else None

    co = pme + pmr if pme is not None and pmr is not None else None
    cf = co - pmpf if co is not None and pmpf is not None else None
    ce = 360 / ge if ge else None

    ncg = ativo_circulante - fornecedores - contas_receber - estoques
    st = ccl - ncg
    cg = ativo_circulante - passivo_circulante

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

def obter_indicadores_empresas(empresas, trimestre_atual, trimestre_anterior):
    """Retorna um DataFrame com todos os indicadores das empresas para o trimestre_atual."""
    resultados = []
    for empresa in empresas:
        print(f"Processando indicadores para {empresa}...")
        try:
            df_24 = pegar_balanco(empresa, trimestre_atual)
            df_23 = pegar_balanco(empresa, trimestre_anterior)
            if not df_24.empty and not df_23.empty:
                indicadores = calcular_indicadores(df_24, df_23)
                indicadores['empresa'] = empresa
                indicadores['trimestre'] = trimestre_atual
                resultados.append(indicadores)
            else:
                print(f"⚠️ Dados insuficientes para {empresa}.")
        except Exception as e:
            print(f"Erro ao processar {empresa}: {e}")
    return pd.DataFrame(resultados)

# Exemplo de uso:
empresas = ['LREN3', 'CEAB3', 'GUAR3', 'AMAR3']
trimestre_atual = '20234T'
trimestre_anterior = '20233T'

df_indicadores = obter_indicadores_empresas(empresas, trimestre_atual, trimestre_anterior)
print(df_indicadores)

# Função para calcular indicadores de comparação entre empresas
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

def main():
    list_tickers = ['LREN3', 'CEAB3', 'GUAR3', 'AMAR3']
    list_tri = ["20243T"]
    df_comparacao = pd.DataFrame()
    for ticker in list_tickers:
        for trimestre in list_tri:
            # ticker = "EZTC3"
            # trimestre = "20234T"
            df = pegar_balanco(ticker, trimestre)
            comparacao = indicador_comparacao(df)
            df_final = pd.DataFrame()
            df_final["ticker"]=[ticker]
            df_final["roe"]=comparacao["roe"]
            df_final["eva"]=comparacao["eva"]
            df_comparacao = pd.concat([df_comparacao, df_final], axis=0,ignore_index=True)
        print(df_comparacao)

# main()

#teste pegar preco corrigido
def pegar_preco_corrigido(ticker, data_inicial, data_final):
    params = {
        'ticker': ticker,
        'data_inicial': data_inicial,
        'data_final': data_final
    }
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUwOTM0ODEyLCJpYXQiOjE3NDgzNDI3ODQsImp0aSI6IjEwODkzOTVmZWUxODRhNDJhNGU0NDc1MGM3ZDAwMjFmIiwidXNlcl9pZCI6NjZ9.LIlgZXw3GMaSzx-aBSQC50cJSZDn0UVk-zc1bZJotHE"
    headers = {'Authorization': 'JWT {}'.format(token)}
    url = 'https://laboratoriodefinancas.com/api/v1/preco-corrigido'
    r = requests.get(url, params=params, headers=headers)
    resposta = r.json()
    if 'dados' in resposta:
        return pd.DataFrame(resposta['dados'])
    else:
        print("⚠️ Resposta da API não contém 'dados':", resposta)
        return pd.DataFrame()
    
def pegar_preco_diversos(ticker, data_inicial, data_final):
    import requests
    import pandas as pd
    params = {
        'ticker': ticker,
        'data_inicial': data_inicial,
        'data_final': data_final
    }
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUwOTM0ODEyLCJpYXQiOjE3NDgzNDI3ODQsImp0aSI6IjEwODkzOTVmZWUxODRhNDJhNGU0NDc1MGM3ZDAwMjFmIiwidXNlcl9pZCI6NjZ9.LIlgZXw3GMaSzx-aBSQC50cJSZDn0UVk-zc1bZJotHE"
    headers = {'Authorization': 'JWT {}'.format(token)}
    url = 'https://laboratoriodefinancas.com/api/v1/preco-diversos'
    r = requests.get(url, params=params, headers=headers)
    resposta = r.json()
    if 'dados' in resposta:
        return pd.DataFrame(resposta['dados'])
    else:
        print("⚠️ Resposta da API não contém 'dados':", resposta)
        return pd.DataFrame()