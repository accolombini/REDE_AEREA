# Documentação do Sistema Integrado de Priorizacão de Ativos

## Visão Geral
Este projeto é uma solução integrada desenvolvida para **analisar e priorizar ativos de rede aérea** com base em critérios de criticidade. Utilizando módulos Python modulares, o sistema permite gerar bases de dados, validar e aplicar pesos personalizados, calcular índices de criticidade e gerar relatórios interativos.

O objetivo principal é criar uma ferramenta flexível e eficiente para tomada de decisões sobre manutenção e priorização de ativos.

---

## Estrutura do Projeto

```plaintext
DADOS/                            # Diretório para arquivos de dados
    interrupcoes_light.csv        # Base de dados principal
    pesos_anal_criticidade.csv    # Pesos iniciais para análise de criticidade
    matriz_priorizacao.csv        # Resultado final da matriz de priorização
    resultado_criticidade.csv     # Resultado detalhado do índice de criticidade

scripts/                          # Diretório para os scripts principais
    geracao_base_dados.py         # Gera base de dados simulada
    pesos_analise_criticidade.py  # Manipula e valida os pesos de criticidade
    eda_analise_estatitica_descritiva_light.py # Realiza EDA e estatística descritiva
    criterio_definido_classificar_criticidade.py # Calcula e classifica criticidade
    matriz_prioridade.py          # Gera matriz de priorização interativa
    integrando_sistema.py         # Script principal integrando todas as etapas

README.md                        # Documentação do projeto
```

---

## Requisitos

### Ambiente e Dependências

1. **Python 3.12**
2. **Bibliotecas Python**
   - `pandas`
   - `numpy`
   - `plotly`
   - `os` (nativo)

### Instalação das Dependências

Use o seguinte comando para instalar as dependências necessárias:

```bash
pip install pandas numpy plotly
```

---

## Execução dos Scripts

### 1. Geração da Base de Dados Simulada

O script **`geracao_base_dados.py`** gera uma base simulada com os seguintes campos:
- **Ativo**, **Data_Interrupcao**, **Tempo_Operacao**, **Freq_Falhas**, **Clientes_Afetados**, **Impacto_DEC**, **Impacto_FEC**, **Causa**, **Status_Ativo**.

Execute o script:

```bash
python geracao_base_dados.py
```

Saída esperada:
```plaintext
Base de dados gerada com sucesso em: DADOS/interrupcoes_light.csv
```

---

### 2. Manipulação e Validação dos Pesos

O script **`pesos_analise_criticidade.py`** gera e valida os pesos para o cálculo da criticidade.

Execute o script:

```bash
python pesos_analise_criticidade.py
```

Saída esperada:
```plaintext
Base de pesos gerada e salva com sucesso em: DADOS/pesos_anal_criticidade.csv
Validação bem-sucedida: Todas as variáveis estão presentes na base de dados.
```

---

### 3. Análise Estatística e Exploratória

O script **`eda_analise_estatitica_descritiva_light.py`** realiza análise exploratória e estatística descritiva da base.

Execute o script:

```bash
python eda_analise_estatitica_descritiva_light.py
```

Saída esperada:
- Relatório no terminal
- Gráficos interativos para visualização dos dados

---

### 4. Cálculo e Classificação da Criticidade

O script **`criterio_definido_classificar_criticidade.py`** calcula os índices de criticidade baseado nos pesos definidos.

Execute o script:

```bash
python criterio_definido_classificar_criticidade.py
```

Saída esperada:
```plaintext
Relatório Final de Criticidade dos Ativos:
Ativo      Criticidade_Calculada
...
```

---

### 5. Geração da Matriz de Priorizção

O script **`matriz_prioridade.py`** gera a matriz de priorização de ativos, com resultados interativos em **Plotly**.

Execute o script:

```bash
python matriz_prioridade.py
```

Saída esperada:
- **Matriz interativa de priorização** em uma interface gráfica.
- Resultado salvo em: `DADOS/matriz_priorizacao.csv`

---

### 6. Sistema Integrado

O script **`integrando_sistema.py`** é a solução final que integra todas as etapas anteriores.

Execute o script:

```bash
python integrando_sistema.py
```

Saída esperada:
```plaintext
### Executando Sistema Integrado ###

Base de dados já existente. Prosseguindo...
Base de pesos existente. Prosseguindo...
Validação bem-sucedida: Todas as variáveis estão presentes na base de dados.

### Sistema Integrado Finalizado com Sucesso ###
```

---

## Resultados

Os arquivos finais serão armazenados no diretório **DADOS**:

- **`interrupcoes_light.csv`**: Base de dados principal.
- **`pesos_anal_criticidade.csv`**: Pesos aplicados para cálculo da criticidade.
- **`matriz_priorizacao.csv`**: Matriz de priorização gerada.
- **`resultado_criticidade.csv`**: Resultado detalhado dos índices de criticidade calculados.

---

## Melhorias Futuras

1. **Testes Automatizados**: Implementar testes unitários para cada módulo.
2. **Integração com NodeJS**: Criar uma API RESTful para acesso aos resultados.
3. **Dashboards Dinâmicos**: Utilizar Plotly Dash ou PowerBI para visualização.

---
