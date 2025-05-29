from modulo import(pegar_balanco, indicador_comparacao, pegar_preco_corrigido, pegar_preco_diversos, obter_indicadores_empresas)
import pandas as pd
import requests
import matplotlib.pyplot as plt

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
def comparar_retorno_ticker_ibov(ticker, data_inicial, data_final):
    """
    Compara o retorno de um ticker e do IBOV no período informado.
    Parâmetros:
        ticker (str): Código do ativo (ex: 'LREN3')
        data_inicial (str): Data inicial no formato 'YYYY-MM-DD'
        data_final (str): Data final no formato 'YYYY-MM-DD'
    """
    # IBOV
    df_ibov = pegar_preco_diversos("ibov", data_inicial, data_final)
    if not df_ibov.empty:
        preco_inicial_ibov = df_ibov.iloc[0]["fechamento"]
        preco_final_ibov = df_ibov.iloc[-1]["fechamento"]
        lucro_ibov = (preco_final_ibov / preco_inicial_ibov) - 1
        print(f"Retorno do IBOV no período de {data_inicial} a {data_final}: {lucro_ibov:.2%}")
    else:
        print("⚠️ Não foi possível obter dados do IBOV.")

    # Ticker escolhido
    df_preco = pegar_preco_corrigido(ticker, data_inicial, data_final)
    if not df_preco.empty:
        preco_inicial = df_preco.iloc[0]["fechamento"]
        preco_final = df_preco.iloc[-1]["fechamento"]
        lucro = (preco_final / preco_inicial) - 1
        print(f"Retorno do ativo {ticker} no período de {data_inicial} a {data_final}: {lucro:.2%}")
    else:
        print(f"⚠️ Não foi possível obter dados de {ticker}.")

#backteste de 1 ano
comparar_retorno_ticker_ibov("LREN3", "2023-04-01", "2024-03-31")
comparar_retorno_ticker_ibov("CEAB3", "2023-04-01", "2024-03-31")
comparar_retorno_ticker_ibov("GUAR3", "2023-04-01", "2024-03-31")
comparar_retorno_ticker_ibov("AMAR3", "2023-04-01", "2024-03-31")

#backteste de 5 anos 
comparar_retorno_ticker_ibov("LREN3", "2019-04-01", "2024-03-31")
comparar_retorno_ticker_ibov("CEAB3", "2019-04-01", "2024-03-31")
comparar_retorno_ticker_ibov("GUAR3", "2019-04-01", "2024-03-31")
comparar_retorno_ticker_ibov("AMAR3", "2019-04-01", "2024-03-31")

#Backteste de 10 anos
comparar_retorno_ticker_ibov("LREN3", "2014-04-01", "2024-03-31")
comparar_retorno_ticker_ibov("CEAB3", "2014-04-01", "2024-03-31")
comparar_retorno_ticker_ibov("GUAR3", "2014-04-01", "2024-03-31")
comparar_retorno_ticker_ibov("AMAR3", "2014-04-01", "2024-03-31")

def calcular_retorno_acumulado(df):
    """Retorna uma série de retorno acumulado (%) ao longo do tempo."""
    df = df.sort_values("data")
    df["retorno"] = df["fechamento"].pct_change().fillna(0)
    df["retorno_acumulado"] = (1 + df["retorno"]).cumprod() - 1
    return df[["data", "retorno_acumulado"]]

tickers = ["LREN3", "CEAB3", "GUAR3", "AMAR3", "ibov"]
data_inicial = "2014-04-01"
data_final = "2024-03-31"

#teste de grafico 
def plotar_retorno_acumulado(tickers, data_inicial, data_final):
    plt.figure(figsize=(12, 7))

    for ticker in tickers:
        if ticker.lower() == "ibov":
            df = pegar_preco_diversos(ticker, data_inicial, data_final)
        else:
            df = pegar_preco_corrigido(ticker, data_inicial, data_final)
        if not df.empty:
            df["data"] = pd.to_datetime(df["data"])
            serie = calcular_retorno_acumulado(df)
            plt.plot(serie["data"], serie["retorno_acumulado"]*100, label=ticker.upper())
        else:
            print(f"⚠️ Não foi possível obter dados de {ticker}.")

    plt.title(f"Retorno acumulado diário dos ativos e IBOV ({data_inicial} a {data_final})")
    plt.xlabel("Data")
    plt.ylabel("Retorno acumulado (%)")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()

# Exemplo de uso:
tickers = ["LREN3", "CEAB3", "GUAR3", "AMAR3", "ibov"]
data_inicial = "2014-04-01"
data_final = "2024-03-31"
plotar_retorno_acumulado(tickers, data_inicial, data_final)

