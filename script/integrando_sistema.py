'''
    REDE_AEREA.DOCX

    |> Objstivo: este script integra todo ciclo de solução abordado neste estudo

    |> Importação dos Módulos Existentes:
        geracao_base_dados.py → Para gerar a base inicial.
        pesos_analise_criticidade.py → Para carregar e validar os pesos.
        criterio_definido_classificar_criticidade.py → Para cálculo da criticidade.
        eda_analise_estatitica_descritiva_light.py → Para análise exploratória.
        matriz_prioridade.py → Para geração da matriz de priorização.

    |> Execução Sequencial Integrada:
        Gerar a base (caso necessário).
        Carregar pesos e validar a base.
        Calcular o índice de criticidade.
        Gerar estatísticas descritivas.
        Apresentar a matriz de priorização em gráfico e salvar os resultados.
'''

# Importar bibliotecas

import os
import pandas as pd
from pesos_analise_criticidade import gerar_pesos_iniciais, validar_pesos
from geracao_base_dados import gerar_base_simulada

# Caminhos para arquivos
OUTPUT_PATH = "/Users/accol/Library/Mobile Documents/com~apple~CloudDocs/UNIVERSIDADES/UFF/PROJETOS/LIGHT/REDE_ATIVOS/REDE_AEREA/script/DADOS"
BASE_FILE_PATH = os.path.join(OUTPUT_PATH, "interrupcoes_light.csv")
PESOS_FILE_PATH = os.path.join(OUTPUT_PATH, "pesos_anal_criticidade.csv")


def main():
    """
    Script principal que integra a geração da base, os pesos e validação.
    """
    print("### Executando Sistema Integrado ###\n")

    # Gerar base de dados simulada
    if not os.path.exists(BASE_FILE_PATH):
        print("Gerando a base de dados simulada...\n")
        gerar_base_simulada(BASE_FILE_PATH)
    else:
        print("Base de dados já existente. Prosseguindo...\n")

    # Gerar ou carregar os pesos
    if not os.path.exists(PESOS_FILE_PATH):
        print("Gerando a base de pesos iniciais...\n")
        gerar_pesos_iniciais()
    else:
        print("Base de pesos existente. Prosseguindo...\n")

    # Validar os pesos com a base de dados
    print("Validando os pesos com a base de dados...\n")
    validar_pesos(BASE_FILE_PATH, pd.read_csv(PESOS_FILE_PATH))

    print("\n### Sistema Integrado Finalizado com Sucesso ###")


if __name__ == "__main__":
    main()
