'''
    ATIVOS_REDE_AEREA.docx
    
    |> Objetivo do script é gerar uma base de dados "realista" para gerarmos alguns testes utilizando Python
    
    |> O que o script faz:
        Gera uma base de 200 registros simulados com dados realistas.
        Salva o arquivo em formato .csv no diretório configurado.
        Cria dados variados e coerentes para testes, facilitando a construção da aplicação Python.
    
    |> A base incluirá as seguintes colunas:
        Trecho: Identificação do trecho.
        Ativo: Tipo de ativo.
        Data_Interrupcao: Data da interrupção.
        Tempo_Operacao: Tempo em operação (anos).
        Freq_Falhas: Número de falhas simuladas.
        Clientes_Afetados: Número de clientes afetados.
        Impacto_DEC: Impacto no DEC.
        Impacto_FEC: Impacto no FEC.
        Causa: Causa da interrupção.
        Status_Ativo: Status operacional.
'''

# Importar bibliotecas
import pandas as pd
import random
import numpy as np
from datetime import datetime, timedelta

# Configurar caminho da pasta DADOS
output_path = "/Users/accol/Library/Mobile Documents/com~apple~CloudDocs/UNIVERSIDADES/UFF/PROJETOS/LIGHT/REDE_ATIVOS/REDE_AEREA/script/DADOS/interrupcoes_light.csv"

# Parâmetros para gerar dados
ativos = ["Transformador", "Religador",
          "Seccionalizador", "Chave", "Regulador"]
causas = ["Falha Técnica", "Clima",
          "Falha Humana", "Animal", "Desgaste Natural"]
status = ["Operacional", "Em Manutenção", "Substituído"]

# Função para gerar datas aleatórias


def gerar_datas(qtd, inicio="2023-01-01", fim="2024-12-31"):
    data_inicio = datetime.strptime(inicio, "%Y-%m-%d")
    data_fim = datetime.strptime(fim, "%Y-%m-%d")
    return [data_inicio + timedelta(days=random.randint(0, (data_fim - data_inicio).days)) for _ in range(qtd)]

# Função para gerar variáveis com distribuição lognormal


def gerar_lognormal(qtd, media, sigma, outlier_ratio=0.05):
    valores = np.random.lognormal(mean=media, sigma=sigma, size=qtd)
    # Adicionar outliers
    n_outliers = int(outlier_ratio * qtd)
    for _ in range(n_outliers):
        valores[random.randint(0, qtd-1)] *= random.uniform(2, 4)
    return valores

# Função para gerar Impacto_DEC baseado em Duração e Clientes Afetados


def gerar_impacto_dec(duracao, clientes_afetados):
    return np.round((duracao / 600) * (clientes_afetados / 2000) * random.uniform(0.5, 2.5), 2)

# Função para gerar Impacto_FEC baseado em Frequência de Falhas e Clientes Afetados


def gerar_impacto_fec(freq_falhas, clientes_afetados):
    return np.round((freq_falhas / 10) * (clientes_afetados / 1500) * random.uniform(0.5, 2.0), 2)

# Função principal para gerar a base de dados


def gerar_base_simulada(output_path, qtd_registros=200):
    print("Gerando base de dados simulada...")

    # Gerar variáveis com distribuições realistas
    tempo_operacao = gerar_lognormal(
        qtd_registros, media=3, sigma=0.7, outlier_ratio=0.05)
    clientes_afetados = gerar_lognormal(
        qtd_registros, media=7, sigma=1, outlier_ratio=0.05)
    freq_falhas = np.random.randint(1, 10, size=qtd_registros)

    # Construir base de dados
    dados = {
        "Trecho": [f"Trecho {i+1}" for i in range(qtd_registros)],
        "Ativo": [random.choice(ativos) for _ in range(qtd_registros)],
        "Data_Interrupcao": gerar_datas(qtd_registros),
        "Tempo_Operacao": np.round(tempo_operacao, 0).astype(int),
        "Freq_Falhas": freq_falhas,
        "Clientes_Afetados": np.round(clientes_afetados, 0).astype(int),
        "Impacto_DEC": [gerar_impacto_dec(d, c) for d, c in zip(tempo_operacao, clientes_afetados)],
        "Impacto_FEC": [gerar_impacto_fec(f, c) for f, c in zip(freq_falhas, clientes_afetados)],
        "Causa": [random.choice(causas) for _ in range(qtd_registros)],
        "Status_Ativo": [random.choice(status) for _ in range(qtd_registros)]
    }

    # Criar DataFrame
    df = pd.DataFrame(dados)

    # Salvar em CSV
    df.to_csv(output_path, index=False, encoding="utf-8")
    print(f"Base de dados gerada com sucesso: {output_path}")

    # Exibir estatísticas finais
    print("\nEstatísticas da Base Gerada:")
    print(df.describe())
    print("\nColunas da Base:")
    print(df.head())


# Executar geração da base de dados
if __name__ == "__main__":
    gerar_base_simulada(output_path)
