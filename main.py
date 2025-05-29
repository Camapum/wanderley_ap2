from modulo import(pegar_balanco, indicador_comparacao, pegar_preco_corrigido, pegar_preco_diversos, obter_indicadores_empresas)
import pandas as pd
import requests
#parametros para pegar balanço
params = {'ticker': 'AZZA','ano_tri': '20244T',}
r = requests.get('https://laboratoriodefinancas.com/api/v1/balanco',params=params, headers=headers)
dados = r.json()['dados'][0]
balanco = dados['balanco']
df_24 = pd.DataFrame(balanco)

params = {'ticker': 'AZZA','ano_tri': '20234T',}
r = requests.get('https://laboratoriodefinancas.com/api/v1/balanco',params=params, headers=headers)
dados = r.json()['dados'][0]
balanco = dados['balanco']
df_23 = pd.DataFrame(balanco)

#pegar_balanço
balanco_renner = pegar_balanco('LREN3', '20234T')
balanco_cea = pegar_balanco('CEAB3', '20234T')
balanco_guar = pegar_balanco('GUAR3', '20234T')
balanco_amar = pegar_balanco('AMAR3', '20234T')

print(balanco_renner)
print(balanco_cea)
print(balanco_guar)
print(balanco_amar)

#pegar_indicadores
empresas = ['LREN3', 'CEAB3', 'GUAR3', 'AMAR3']
trimestre_atual = '20234T'
trimestre_anterior = '20233T'

df_indicadores = obter_indicadores_empresas(empresas, trimestre_atual, trimestre_anterior)
print(df_indicadores)


#função com calculo de roe e eva
def main():
    list_tickers = ['LREN3', 'CEAB3', 'GUAR3', 'AMAR3']
    list_tri = ["20244T"]
    df_comparacao = pd.DataFrame()
    for ticker in list_tickers:
        for trimestre in list_tri:
            # ticker = "EZTC3"
            # trimestre = "20244T"
            df = pegar_balanco(ticker, trimestre)
            comparacao = indicador_comparacao(df)
            df_final = pd.DataFrame()
            df_final["ticker"]=[ticker]
            df_final["roe"]=comparacao["roe"]
            df_final["eva"]=comparacao["eva"]
            df_comparacao = pd.concat([df_comparacao, df_final], axis=0,ignore_index=True)
        print(df_comparacao)

main()

#Backteste
ticker = "LREN3"
data_inicial = "2023-04-01"
data_final = "2024-03-31"
df_preco = pegar_preco_corrigido(ticker, data_inicial, data_final)
preco_inicial = df_preco[0:1]["fechamento"].iloc[0]
preco_final = df_preco[-1:]["fechamento"].iloc[0]
lucro = (preco_final/preco_inicial) - 1
print(f"Retorno do ativo {ticker} no periodo de {data_inicial} a {data_final}: {lucro:.2%}")

ticker = "ibov"
df_ibov = pegar_preco_diversos(ticker, data_inicial, data_final)
preco_inicial_ibov = df_ibov[0:1]["fechamento"].iloc[0]
preco_final_ibov = df_ibov[-1:]["fechamento"].iloc[0]
lucro_ibov = (preco_final_ibov/preco_inicial_ibov) - 1
print(f"Retorno do ibov no periodo de {data_inicial} a {data_final}: {lucro_ibov:.2%}")