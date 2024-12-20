'''
    ATIVOS_REDE_AEREA.docx
    Este script é um ensaio para trabalhar com a definição de critérios para a classificação da criticidade.

        ||> Objetivo Geral do Script
            O script tem como propósito avaliar a criticidade de ativos (por exemplo, equipamentos de média tensão) utilizando dados simulados.
            Leitura dos pesos diretamente do arquivo "pesos_anal_criticidade.csv" e inclusão da variável Impacto_FEC.

        ||> Metodologia Atualizada
            1. Carregar dados e pesos externos.
            2. Validação automática entre pesos e colunas do DataFrame.
            3. Cálculo do Índice de Criticidade, incluindo Impacto_FEC.
            4. Visualizações interativas: mapa de calor, comparação entre criticidade calculada e real, ranking e tabela interativa.
'''

# Importar bibliotecas
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os

# Caminho dos arquivos
output_path = "/Users/accol/Library/Mobile Documents/com~apple~CloudDocs/UNIVERSIDADES/UFF/PROJETOS/LIGHT/REDE_ATIVOS/REDE_AEREA/script/DADOS"
pesos_file_path = os.path.join(output_path, "pesos_anal_criticidade.csv")
base_dados_path = os.path.join(output_path, "interrupcoes_light.csv")

# 1. Carregar os Dados e Pesos


def carregar_dados_pesos(base_path, pesos_path):
    df = pd.read_csv(base_path)
    pesos_df = pd.read_csv(pesos_path)
    print("Base de dados e pesos carregados com sucesso!")
    return df, pesos_df

# 2. Validar Pesos com a Base de Dados


def validar_pesos(df, pesos_df):
    variaveis_base = df.columns.tolist()
    variaveis_pesos = pesos_df["Variavel"].tolist()
    variaveis_faltantes = [
        var for var in variaveis_pesos if var not in variaveis_base]
    if variaveis_faltantes:
        raise ValueError(f"Variáveis faltantes na base de dados: {
                         variaveis_faltantes}")
    print("Validação bem-sucedida: Todas as variáveis estão presentes na base de dados.")

# 3. Calcular Criticidade com Pesos


def calcular_criticidade(df, pesos_df):
    pesos_dict = dict(zip(pesos_df["Variavel"], pesos_df["Peso"]))
    df["Criticidade_Calculada"] = sum(
        df[var] * pesos_dict.get(var, 0) for var in pesos_dict
    )
    return df.sort_values(by="Criticidade_Calculada", ascending=False)

# 4. Visualizações dos Resultados


def gerar_graficos(df):
    # Gráfico 1: Heatmap de Correlação (excluindo colunas não numéricas)
    colunas_numericas = df.select_dtypes(include=[np.number]).columns.tolist()
    corr_matrix = df[colunas_numericas].corr()
    fig_heatmap = px.imshow(
        corr_matrix, text_auto=True, color_continuous_scale="RdBu_r",
        title="Correlação entre Variáveis", labels=dict(color="Correlação")
    )
    fig_heatmap.show()

    # Gráfico 2: Comparacão entre Criticidade Calculada e Real
    if "Criticidade_REAL" in df.columns:
        fig_comparativo = px.bar(
            df, x="Ativo", y=["Criticidade_Calculada", "Criticidade_REAL"],
            title="Comparacão entre Criticidade Calculada e Real",
            barmode="group", labels={"value": "Criticidade", "variable": "Tipo"},
            text_auto=True
        )
        fig_comparativo.show()

    # Gráfico 3: Ranking dos Ativos
    fig_ranking = px.bar(
        df, x="Ativo", y="Criticidade_Calculada",
        title="Ranking dos Ativos pela Criticidade Calculada",
        text="Criticidade_Calculada",
        labels={"Criticidade_Calculada": "Índice de Criticidade"}
    )
    fig_ranking.update_traces(
        texttemplate='%{text:.2f}', textposition='outside')
    fig_ranking.show()

    # Gráfico 4: Tabela Interativa
    fig_table = go.Figure(
        data=[go.Table(
            columnwidth=[10, 5, 5, 5, 5, 5],
            header=dict(values=[
                "<b>Ativo</b>", "<b>Freq. Falhas</b>", "<b>Tempo Operação</b>",
                "<b>Impacto DEC</b>", "<b>Impacto FEC</b>", "<b>Criticidade Calculada</b>"
            ], fill_color='lightgrey', line_color='darkslategray', align='center', font=dict(size=12, color='black')),
            cells=dict(values=[
                df["Ativo"], df["Freq_Falhas"], df["Tempo_Operacao"],
                df["Impacto_DEC"], df["Impacto_FEC"], np.round(
                    df["Criticidade_Calculada"], 2)
            ], fill_color='white', line_color='darkslategray', align='center', font=dict(size=12, color='black'))
        )]
    )
    fig_table.update_layout(
        title_text="Tabela de Criticidade dos Ativos", title_x=0.5, margin=dict(l=10, r=10, t=50, b=10), width=800
    )
    fig_table.show()


# 5. Executar o Script Principal
if __name__ == "__main__":
    # Carregar dados e pesos
    df, pesos_df = carregar_dados_pesos(base_dados_path, pesos_file_path)

    # Validar pesos
    validar_pesos(df, pesos_df)

    # Calcular criticidade
    df = calcular_criticidade(df, pesos_df)

    # Relatório no terminal
    print("\nRelatório Final de Criticidade dos Ativos:")
    print(df[["Ativo", "Criticidade_Calculada"]])

    # Gerar gráficos e tabelas
    gerar_graficos(df)

    # Salvar resultado final
    resultado_path = os.path.join(output_path, "resultado_criticidade.csv")
    df.to_csv(resultado_path, index=False)
    print(f"Resultados salvos em: {resultado_path}")
