''' 
    REDE_AEREA.docx

    Script para gerar uma base de pesos que será usada na análise de criticidade dos ativos.

    |> Atualizações:
        1. Adição da variável Impacto_FEC.
        2. Validação automática entre os pesos e as colunas da base de dados.
        3. Flexibilidade para modificar os pesos interativamente.
'''

# Importar bibliotecas
import pandas as pd
import os

# Caminho para o diretório de saída
OUTPUT_PATH = "/Users/accol/Library/Mobile Documents/com~apple~CloudDocs/UNIVERSIDADES/UFF/PROJETOS/LIGHT/REDE_ATIVOS/REDE_AEREA/script/DADOS"
PESOS_FILE_PATH = os.path.join(OUTPUT_PATH, "pesos_anal_criticidade.csv")
BASE_FILE_PATH = os.path.join(OUTPUT_PATH, "interrupcoes_light.csv")


def gerar_pesos_iniciais():
    """
    Gera e salva a base inicial de pesos em um arquivo CSV.
    """
    pesos_data = {
        "Variavel": ["Freq_Falhas", "Tempo_Operacao", "Impacto_DEC", "Impacto_FEC", "Clientes_Afetados"],
        "Peso": [0.00, 0.08, 32.43, 20.15, 0.04]
    }

    # Criar DataFrame de pesos
    pesos_df = pd.DataFrame(pesos_data)

    # Garantir que o diretório existe
    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH)

    # Salvar arquivo
    pesos_df.to_csv(PESOS_FILE_PATH, index=False, encoding="utf-8")
    print(f"Base de pesos gerada e salva com sucesso em: {PESOS_FILE_PATH}\n")
    return pesos_df


def exibir_pesos(pesos_df):
    """
    Exibe os pesos no terminal.
    """
    print("Pesos Iniciais da Análise de Criticidade:")
    print(pesos_df)


def validar_pesos(base_path, pesos_df):
    """
    Valida se as variáveis no arquivo de pesos existem na base de dados.
    """
    if not os.path.exists(base_path):
        print("Base de dados não encontrada para validação.")
        return

    # Carregar base de dados
    df = pd.read_csv(base_path)
    colunas_base = df.columns.tolist()

    # Variáveis faltantes
    variaveis_faltantes = [
        var for var in pesos_df["Variavel"] if var not in colunas_base]
    if variaveis_faltantes:
        print("\nAviso: As seguintes variáveis estão nos pesos, mas não existem na base de dados:")
        print(variaveis_faltantes)
    else:
        print(
            "\nValidação bem-sucedida: Todas as variáveis estão presentes na base de dados.")


def main():
    """
    Função principal para execução.
    """
    # Gerar ou carregar pesos
    if os.path.exists(PESOS_FILE_PATH):
        pesos_df = pd.read_csv(PESOS_FILE_PATH)
        print("Base de pesos carregada com sucesso!\n")
    else:
        pesos_df = gerar_pesos_iniciais()

    # Exibir pesos no terminal
    exibir_pesos(pesos_df)

    # Validar os pesos com a base de dados
    validar_pesos(BASE_FILE_PATH, pesos_df)


if __name__ == "__main__":
    main()
