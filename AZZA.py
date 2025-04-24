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

intagivel = valor_contabil(df_24, '^1.*','^Intang*')
imobilizado = valor_contabil(df_24, '^1.*', 'Imobilizados')
investimentos = valor_contabil(df_24, '^1.*', 'Invest')
pl = valor_contabil(df_24, '^2.*', 'patrim.nio')

ipl = (intagivel + imobilizado + investimentos) / pl

estoque_24 = valor_contabil(df_24, '^1.0*', 'estoque')
estoque_23 = valor_contabil(df_23, '^1.0*', 'estoque')

estoque_medio = (estoque_24 + estoque_23) / 2

# Indicadores de Liquidez
ativo_circulante = valor_contabil(df_24, '^1.01', '')  # Ativo Circulante
ativo_nao_circulante = valor_contabil(df_24, '^1.1', '')  # Ativo Não Circulante
passivo_circulante = valor_contabil(df_24, '^2.01', '')  # Passivo Circulante
passivo_nao_circulante = valor_contabil(df_24, '^2.02', '')  # Passivo Não Circulante
disponibilidades = valor_contabil(df_24, '^1.01', 'Caixa|Bancos')  # Caixa e equivalentes
estoques = valor_contabil(df_24, '^1.01', 'estoque')
realizavel_curto_prazo = ativo_circulante - estoques - disponibilidades

# Liquidez
ccl = ativo_circulante - passivo_circulante  # Capital Circulante Líquido
lc = ativo_circulante / passivo_circulante if passivo_circulante else None  # Liquidez Corrente
ls = (ativo_circulante - estoques) / passivo_circulante if passivo_circulante else None  # Liquidez Seca
li = disponibilidades / passivo_circulante if passivo_circulante else None  # Liquidez Imediata
lg = (ativo_circulante + ativo_nao_circulante) / (passivo_circulante + passivo_nao_circulante)  # Liquidez Geral

# Endividamento
pl = valor_contabil(df_24, '^2.*', 'patrim.nio')
divida_total = passivo_circulante + passivo_nao_circulante
endividamento_geral = divida_total / (ativo_circulante + ativo_nao_circulante)
solvencia = (ativo_circulante + ativo_nao_circulante) / (passivo_circulante + passivo_nao_circulante)
relacao_ct_cp = passivo_nao_circulante / passivo_circulante if passivo_circulante else None
composicao_endividamento = passivo_circulante / divida_total if divida_total else None

# Imobilização
imobilizado = valor_contabil(df_24, '^1.*', 'Imobilizad')
ipl = imobilizado / pl if pl else None

# Estoque e CMV
estoque_medio = (valor_contabil(df_24, '^1.01', 'estoque') + valor_contabil(df_23, '^1.01', 'estoque')) / 2
cmv = valor_contabil(df_24, '^3.*', 'CMV')
pme = 360 * (estoque_medio / cmv) if cmv else None
ge = cmv / estoque_medio if estoque_medio else None

# Prazo Médio
receitas = valor_contabil(df_24, '^3.*', 'Receita')
contas_receber = valor_contabil(df_24, '^1.01', 'Clientes|Duplicatas')
pmr = 360 * contas_receber / receitas if receitas else None
fornecedores = valor_contabil(df_24, '^2.01', 'Fornecedores')
pmpf = 360 * fornecedores / cmv if cmv else None

#Verificação de valores 
if pme is None:
    print("⚠️ PMEs está None — provavelmente por CMV faltando ou zero.")
if pmr is None:
    print("⚠️ PMR está None — verifique receitas ou contas a receber.")
co = pme + pmr if pme is not None and pmr is not None else None


# Ciclos
co = pme + pmr if pme is not None and pmr is not None else None
cf = co - pmpf
ce = 360 / ge if ge else None

# Capital de Giro
ncg = ativo_circulante - fornecedores - contas_receber - estoques
st = ccl - ncg  # Saldo em Tesouraria
cg = ativo_circulante - passivo_circulante
