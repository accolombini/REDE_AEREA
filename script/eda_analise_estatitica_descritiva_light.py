''' 
    ATIVOS_REDE_AEREA.docx

    |> Objetivo: realizar pré-processamento inical nos dados.

    |> O que o Script Faz
        Carrega a Base de Dados:
        Lê o arquivo .csv e converte a coluna Data_Interrupcao para o formato de data.
        Gera Estatísticas Descritivas:
        Resumo dos dados numéricos.
        Gráficos Interativos:
            Interrupções por Tipo de Ativo (Gráfico de barras).
            Distribuição das Causas (Gráfico de pizza).
            Interrupções por Mês (Gráfico temporal).
            Correlação entre Duração e Clientes Afetados (Gráfico de dispersão).
            Boxplot independente para todas as variáveis numéricas.
            Correlação entre o tempo de operação e clientes afetados (gráfico de dispersão).
'''

# Importar as bibliotecas

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Caminho do arquivo
file_path = "/Users/accol/Library/Mobile Documents/com~apple~CloudDocs/UNIVERSIDADES/UFF/PROJETOS/LIGHT/REDE_ATIVOS/REDE_AEREA/script/DADOS/interrupcoes_light.csv"

# 1. Carregar os dados
df = pd.read_csv(file_path, parse_dates=["Data_Interrupcao"])
print("Dados carregados com sucesso!")

# 2. Estatísticas Descritivas
print("\nInformações dos Dados:")
print(df.info())
print("\nEstatísticas Descritivas:")
print(df.describe())

# 3. Gráfico de Barras com Valores no Topo (Quantidade de Interrupções por Ativo)
fig_ativos = px.bar(
    df, x="Ativo", title="Quantidade de Interrupções por Tipo de Ativo", color="Ativo"
)
fig_ativos.show()

# 4. Gráfico de Pizza (Distribuição das Causas)
fig_causas = px.pie(df, names="Causa",
                    title="Distribuição das Causas das Interrupções")
fig_causas.show()

# 5. Gráfico de Ocorrências por Mês
df["Mes_Ano"] = df["Data_Interrupcao"].dt.to_period("M").astype(str)
fig_mes = px.bar(
    df.groupby("Mes_Ano").size().reset_index(name="Quantidade"),
    x="Mes_Ano", y="Quantidade", title="Interrupções por Mês"
)
fig_mes.update_layout(yaxis_title="Quantidade", xaxis_title="Mês/Ano")
fig_mes.show()

# 6. Gráfico de Correlação com Linha de Tendência (Tempo de Operação x Clientes Afetados)
fig_corr = px.scatter(
    df, x="Tempo_Operacao", y="Clientes_Afetados",
    size="Impacto_DEC", color="Ativo",
    trendline="ols",
    title="Correlação entre Tempo de Operação e Clientes Afetados"
)
fig_corr.update_traces(marker=dict(
    line=dict(width=0.5, color='DarkSlateGrey')))
fig_corr.update_layout(xaxis_title="Tempo de Operação (anos)",
                       yaxis_title="Clientes Afetados")
fig_corr.show()

# 7. Boxplots Independentes em Subplots
variaveis_numericas = ["Tempo_Operacao", "Freq_Falhas",
                       "Clientes_Afetados", "Impacto_DEC", "Impacto_FEC"]
fig_boxplots = make_subplots(rows=len(variaveis_numericas), cols=1,
                             subplot_titles=variaveis_numericas)

for i, var in enumerate(variaveis_numericas):
    fig_boxplots.add_trace(
        go.Box(y=df[var], name=var, boxmean='sd'), row=i+1, col=1
    )

fig_boxplots.update_layout(
    title_text="Boxplots Independentes das Variáveis Numéricas",
    height=1500,  # Altura ajustada para acomodar todos os gráficos
    showlegend=False
)
fig_boxplots.show()
