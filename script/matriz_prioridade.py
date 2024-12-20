'''
    ||> ATIVOS_REDE_AEREA.docx
        |||> Esboço de como encaminhar a construção da matriz de priorização

        |> Nota:
            A fórmula utilizada para calcular o Índice de Criticidade segue uma abordagem comum em sistemas de priorização multicritério, MCDM (Multiple-Criteria Decision Making) (atenção é apenas um teste de cenário usando Python). Ela combina variáveis normalizadas com pesos ajustáveis para gerar uma pontuação final, permitindo uma comparação objetiva entre os ativos. Também pode ser aplicada a AHP (Analytic Hierarchy Process): Técnica de priorização usando pesos ajustáveis e em Modelos de Risco e Criticidade: Utilizados em operações de manutenção para avaliação de ativos.

            |> Variáveis:

                Freq. Falhas: Frequência de falhas dos ativos.
                Tempo Operação: Tempo de operação (em anos) dos ativos.
                Impacto DEC/FEC: Contribuição do ativo nos indicadores regulatórios de continuidade.
                Clientes Afetados: Quantidade de clientes impactados pelas falhas.
                
                |> Normalização:

                    Utiliza o método Min-Max Scaling para normalizar os valores entre 0 e 1. A ideia é  garantir que todas as variáveis, independentemente das suas unidades (exemplo: anos, porcentagens, contagens), tenham a mesma importância antes da aplicação dos pesos:

                            VAriNorm = (Valor - Mínimo) / (Máximo - Mínimo)

                    |> Pesos:

                        Pesos fornecidos dinamicamente no arquivo "pesos_anal_criticidade.csv".


||> Atualização no Script
    1. Leitura dos pesos dinamicamente a partir de "pesos_anal_criticidade.csv".
    2. Inclusão de validação automática entre pesos e colunas da base de dados.
    3. Cálculo do Índice de Criticidade atualizado com variáveis reais, incluindo Impacto_FEC.
    4. Geração da coluna "Impacto_DEC_FEC" combinando valores de DEC e FEC.
'''

# Importar bibliotecas
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os

# Caminhos para arquivos
output_path = "/Users/accol/Library/Mobile Documents/com~apple~CloudDocs/UNIVERSIDADES/UFF/PROJETOS/LIGHT/REDE_ATIVOS/REDE_AEREA/script/DADOS"
pesos_file_path = os.path.join(output_path, "pesos_anal_criticidade.csv")
dados_path = os.path.join(output_path, "interrupcoes_light.csv")

# Funções do Script


def carregar_dados_e_pesos(dados_path, pesos_path):
    """
    Carrega a base de dados e os pesos fornecidos no arquivo externo.
    """
    df = pd.read_csv(dados_path)
    pesos_df = pd.read_csv(pesos_path)
    print("Base de dados e pesos carregados com sucesso!\n")
    return df, pesos_df


def validar_pesos(df, pesos_df):
    """
    Valida se todas as variáveis definidas no arquivo de pesos existem na base de dados.
    """
    variaveis_base = df.columns.tolist()
    variaveis_pesos = pesos_df["Variavel"].tolist()
    variaveis_faltantes = [
        var for var in variaveis_pesos if var not in variaveis_base]
    if variaveis_faltantes:
        raise ValueError(f"Variáveis faltantes na base de dados: {
                         variaveis_faltantes}")
    print("Validação bem-sucedida: Todas as variáveis estão presentes na base de dados.\n")


def calcular_criticidade(df, pesos_df):
    """
    Calcula o Índice de Criticidade utilizando os pesos fornecidos.
    """
    # Dicionário de pesos
    pesos_dict = dict(zip(pesos_df["Variavel"], pesos_df["Peso"]))

    # Combinar Impacto_DEC e Impacto_FEC em uma nova coluna
    if "Impacto_DEC" in df.columns and "Impacto_FEC" in df.columns:
        df["Impacto_DEC_FEC"] = df["Impacto_DEC"] + df["Impacto_FEC"]
    else:
        raise KeyError(
            "As colunas 'Impacto_DEC' e 'Impacto_FEC' são necessárias para calcular 'Impacto_DEC_FEC'.")

    # Normalização Min-Max
    for col in pesos_dict.keys():
        if col in df.columns:
            df[col + "_Norm"] = (df[col] - df[col].min()) / \
                (df[col].max() - df[col].min())

    # Cálculo do índice
    df["Indice_Criticidade"] = sum(
        df[col + "_Norm"] * peso for col, peso in pesos_dict.items()
    )

    # Ordena por criticidade
    df = df.sort_values(by="Indice_Criticidade", ascending=False)
    return df


def gerar_matriz_priorizacao(df):
    """
    Gera a tabela interativa da Matriz de Priorizacao usando Plotly.
    """
    fig = go.Figure(
        data=[go.Table(
            columnwidth=[10, 5, 5, 5, 5, 5],
            header=dict(values=[
                "<b>Ativo</b>", "<b>Freq. Falhas (Norm)</b>", "<b>Tempo Operação (Norm)</b>",
                "<b>Impacto DEC/FEC (Norm)</b>", "<b>Índice de Criticidade</b>"
            ], fill_color='lightgrey', align='center'),
            cells=dict(values=[
                df["Ativo"],
                np.round(df.get("Freq_Falhas_Norm", 0), 2),
                np.round(df.get("Tempo_Operacao_Norm", 0), 2),
                np.round(df.get("Impacto_DEC_FEC_Norm", 0), 2),
                np.round(df["Indice_Criticidade"], 2)
            ], fill_color='white', align='center')
        )]
    )
    fig.update_layout(
        title_text="Matriz de Priorizacao dos Ativos",
        title_x=0.5, margin=dict(l=10, r=10, t=50, b=10), width=800
    )
    fig.show()


# Script Principal
if __name__ == "__main__":
    # Carregar dados e pesos
    df, pesos_df = carregar_dados_e_pesos(dados_path, pesos_file_path)

    # Validar os pesos
    validar_pesos(df, pesos_df)

    # Calcular criticidade
    df = calcular_criticidade(df, pesos_df)

    # Exibir matriz no terminal
    print("Matriz de Priorizacao dos Ativos:\n")
    print(df[["Ativo", "Indice_Criticidade"]].to_string(index=False))

    # Gerar matriz interativa
    gerar_matriz_priorizacao(df)

    # Salvar resultados
    resultado_path = os.path.join(output_path, "matriz_priorizacao.csv")
    df.to_csv(resultado_path, index=False)
    print(f"\nResultados salvos em: {resultado_path}")
