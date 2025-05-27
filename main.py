from modulo import(pegar_balanco, indicador_comparacao, pegar_preco_corrigido, pegar_preco_diversos)
import pandas as pd

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
df_preco = pegar_preco_corrigidoS(ticker, data_inicial, data_final)
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