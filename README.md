<<<<<<< HEAD
# Análise Estatística de Dados Laboratoriais (PCR / Valor Ct)

Projecto Python para análise estatística descritiva, geração de tabelas e
gráficos a partir de dados laboratoriais (testes PCR — valores Ct, resultados
Positivo/Negativo, patógeno, laboratório e qualidade da amostra).

## Estrutura do projecto

```
projeto_lab/
├── dados/
│   └── lab_limpo.csv          # dados de entrada
├── src/
│   ├── analise_estatistica.py # cálculo de medidas estatísticas + tabelas
│   ├── graficos.py            # geração de todos os gráficos
│   └── main.py                # script principal (corre tudo)
├── saidas/
│   ├── tabelas/                # CSVs + Excel (multi-folha) com os resultados
│   └── graficos/                # PNGs com os gráficos
├── requirements.txt
└── README.md
```

## Como executar

1. Instalar as dependências:
   ```bash
   pip install -r requirements.txt
   ```

2. Correr o pipeline completo (tabelas + gráficos):
   ```bash
   cd src
   python3 main.py
   ```

   Ou correr cada etapa em separado:
   ```bash
   python3 src/analise_estatistica.py   # só tabelas
   python3 src/graficos.py              # só gráficos
   ```

## Dados de entrada

O ficheiro `dados/lab_limpo.csv` contém 120 amostras com as colunas:

| Coluna              | Descrição                                   |
|---------------------|----------------------------------------------|
| id_amostra          | Identificador único da amostra                |
| id_paciente         | Identificador único do paciente                |
| patogeno            | Patógeno testado (COVID-19 / Influenza)        |
| valor_ct            | Valor Ct do teste PCR (numérico)               |
| resultado           | Resultado do teste (Positivo / Negativo)       |
| data_teste          | Data em que o teste foi realizado              |
| laboratorio         | Laboratório responsável (Lab1 / Lab2)          |
| qualidade_amostra   | Qualidade da amostra (Boa / Media)             |

## Medidas estatísticas calculadas

Para a variável `valor_ct` (global, por patógeno, por laboratório e por
resultado): N, média, mediana, moda, desvio padrão, variância, mínimo,
máximo, amplitude, quartis (Q1/Q3), IQR, coeficiente de variação,
assimetria, curtose, erro padrão e intervalo de confiança a 95%.

Também são geradas tabelas de frequência, tabelas cruzadas (contingência) e
taxas de positividade por grupo.

## Gráficos gerados

1. Histograma da distribuição do valor Ct
2. Boxplot do valor Ct por patógeno
3. Boxplot do valor Ct por laboratório
4. Barras: número de amostras por patógeno
5. Barras: número de amostras por laboratório
6. Gráfico circular (pizza) de resultados Positivo/Negativo
7. Barras empilhadas: resultado por patógeno
8. Evolução temporal (semanal) do valor Ct médio
9. Gráfico de violino: valor Ct por qualidade da amostra
10. Mapa de calor: taxa de positividade por laboratório x patógeno
11. Painel resumo (dashboard) com 4 gráficos principais

## Resultados principais (resumo)

- Valor Ct médio global: **25,33** (mediana 25,00; desvio padrão 5,65)
- 120 amostras, sem valores em falta
- 79,2% dos testes foram Positivos; 20,8% Negativos
- COVID-19: 66 amostras (55%) | Influenza: 54 amostras (45%)
- Os valores Ct dos resultados Negativos são, em média, bastante mais altos
  (33,6) do que os Positivos (23,2) — coerente com a interpretação clínica
  habitual (Ct mais alto = menos carga viral / resultado negativo).
=======
# -curso-de-Python
esta pasta tem:

##Descrição do Projeto: 
contexto de criação do projecto no ambito do curso de Python...
Aqui estão reunidos exercícios, exemplos e práticas desenvolvidas durante a aprendizagem da linguagem Python.

##Objetivo
O objetivo deste projeto é:
- Aprender os conceitos básicos de programação em Python
- Praticar lógica de programação
- Desenvolver pequenos exercícios e scripts
- Utilizar o Git e GitHub para controlo de versões

##Tecnologias utilizadas
- Python 3
- Git
- GitHub
- VS Code

##Estrutura do projeto
O projeto pode conter:
- Scripts em Python (.py)
- Exercícios práticos
- Notas de estudo
>>>>>>> 7fc08bbd5808b529e375830c0b894eff1d671c99
