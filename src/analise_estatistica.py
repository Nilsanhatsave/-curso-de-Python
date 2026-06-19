"""
Projecto: Análise Estatística de Dados Laboratoriais (Valores Ct - PCR)
=========================================================================
Script principal: calcula medidas estatísticas descritivas e gera
tabelas (CSV/XLSX) com os resultados.

Autor: Gerado com Claude
"""

import pandas as pd
import numpy as np
from scipy import stats
import os

# ---------------------------------------------------------------------------
# Configuração de caminhos
# ---------------------------------------------------------------------------
PASTA_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAMINHO_DADOS = os.path.join(PASTA_BASE, "dados", "lab_limpo.csv")
PASTA_TABELAS = os.path.join(PASTA_BASE, "saidas", "tabelas")

os.makedirs(PASTA_TABELAS, exist_ok=True)


def carregar_dados(caminho=CAMINHO_DADOS):
    """Carrega o ficheiro CSV e faz pequenas conversões de tipo."""
    df = pd.read_csv(caminho)
    df["data_teste"] = pd.to_datetime(df["data_teste"])
    return df


def medidas_descritivas(serie):
    """Calcula um conjunto completo de medidas estatísticas para uma série numérica."""
    n = serie.count()
    media = serie.mean()
    mediana = serie.median()
    moda = serie.mode().iloc[0] if not serie.mode().empty else np.nan
    desvio_padrao = serie.std()
    variancia = serie.var()
    minimo = serie.min()
    maximo = serie.max()
    amplitude = maximo - minimo
    q1 = serie.quantile(0.25)
    q3 = serie.quantile(0.75)
    iqr = q3 - q1
    cv = (desvio_padrao / media) * 100 if media != 0 else np.nan
    assimetria = stats.skew(serie.dropna())
    curtose = stats.kurtosis(serie.dropna())
    erro_padrao = stats.sem(serie.dropna())
    ic95 = stats.t.interval(0.95, n - 1, loc=media, scale=erro_padrao)

    return {
        "N": n,
        "Média": round(media, 3),
        "Mediana": round(mediana, 3),
        "Moda": round(moda, 3),
        "Desvio Padrão": round(desvio_padrao, 3),
        "Variância": round(variancia, 3),
        "Mínimo": round(minimo, 3),
        "Máximo": round(maximo, 3),
        "Amplitude": round(amplitude, 3),
        "Q1 (25%)": round(q1, 3),
        "Q3 (75%)": round(q3, 3),
        "IQR": round(iqr, 3),
        "Coef. Variação (%)": round(cv, 3),
        "Assimetria (Skewness)": round(assimetria, 3),
        "Curtose": round(curtose, 3),
        "Erro Padrão": round(erro_padrao, 3),
        "IC 95% (Inferior)": round(ic95[0], 3),
        "IC 95% (Superior)": round(ic95[1], 3),
    }


def tabela_geral(df):
    """Medidas estatísticas globais para a variável valor_ct."""
    medidas = medidas_descritivas(df["valor_ct"])
    tabela = pd.DataFrame(list(medidas.items()), columns=["Medida", "Valor"])
    return tabela


def tabela_por_grupo(df, coluna_grupo, coluna_valor="valor_ct"):
    """Medidas estatísticas de valor_ct, agrupadas por uma coluna categórica."""
    resultados = []
    for grupo, sub in df.groupby(coluna_grupo):
        medidas = medidas_descritivas(sub[coluna_valor])
        medidas[coluna_grupo] = grupo
        resultados.append(medidas)
    tabela = pd.DataFrame(resultados)
    cols = [coluna_grupo] + [c for c in tabela.columns if c != coluna_grupo]
    return tabela[cols]


def tabela_frequencias(df, coluna):
    """Tabela de frequências absolutas e relativas para uma variável categórica."""
    freq_abs = df[coluna].value_counts()
    freq_rel = df[coluna].value_counts(normalize=True) * 100
    tabela = pd.DataFrame({
        "Frequência Absoluta": freq_abs,
        "Frequência Relativa (%)": freq_rel.round(2),
    })
    tabela.index.name = coluna
    tabela = tabela.reset_index()
    return tabela


def tabela_cruzada(df, linha, coluna):
    """Tabela cruzada (contingência) entre duas variáveis categóricas."""
    return pd.crosstab(df[linha], df[coluna], margins=True, margins_name="Total")


def taxa_positividade_por_grupo(df, coluna_grupo):
    """Calcula a taxa de positividade (%) por grupo (laboratório, patógeno, etc.)."""
    resultado = (
        df.groupby(coluna_grupo)["resultado"]
        .apply(lambda x: (x == "Positivo").mean() * 100)
        .round(2)
        .reset_index(name="Taxa de Positividade (%)")
    )
    return resultado


def executar_analise():
    print("A carregar dados...")
    df = carregar_dados()
    print(f"Dataset carregado: {df.shape[0]} amostras, {df.shape[1]} colunas.\n")

    # 1. Medidas estatísticas gerais (valor_ct)
    print("Calculando medidas estatísticas gerais do valor Ct...")
    tab_geral = tabela_geral(df)
    tab_geral.to_csv(os.path.join(PASTA_TABELAS, "01_estatisticas_gerais.csv"), index=False)
    print(tab_geral.to_string(index=False))
    print()

    # 2. Medidas por patógeno
    print("Calculando medidas estatísticas por patógeno...")
    tab_patogeno = tabela_por_grupo(df, "patogeno")
    tab_patogeno.to_csv(os.path.join(PASTA_TABELAS, "02_estatisticas_por_patogeno.csv"), index=False)
    print(tab_patogeno.to_string(index=False))
    print()

    # 3. Medidas por laboratório
    print("Calculando medidas estatísticas por laboratório...")
    tab_lab = tabela_por_grupo(df, "laboratorio")
    tab_lab.to_csv(os.path.join(PASTA_TABELAS, "03_estatisticas_por_laboratorio.csv"), index=False)
    print(tab_lab.to_string(index=False))
    print()

    # 4. Medidas por resultado (Positivo/Negativo)
    print("Calculando medidas estatísticas por resultado...")
    tab_resultado = tabela_por_grupo(df, "resultado")
    tab_resultado.to_csv(os.path.join(PASTA_TABELAS, "04_estatisticas_por_resultado.csv"), index=False)
    print(tab_resultado.to_string(index=False))
    print()

    # 5. Tabelas de frequência para variáveis categóricas
    print("Gerando tabelas de frequência...")
    for col in ["patogeno", "resultado", "laboratorio", "qualidade_amostra"]:
        tab_freq = tabela_frequencias(df, col)
        tab_freq.to_csv(os.path.join(PASTA_TABELAS, f"05_frequencia_{col}.csv"), index=False)
        print(f"\n-- {col} --")
        print(tab_freq.to_string(index=False))
    print()

    # 6. Tabela cruzada patógeno x resultado
    print("Gerando tabela cruzada patógeno x resultado...")
    tab_cruz1 = tabela_cruzada(df, "patogeno", "resultado")
    tab_cruz1.to_csv(os.path.join(PASTA_TABELAS, "06_cruzamento_patogeno_resultado.csv"))
    print(tab_cruz1.to_string())
    print()

    # 7. Tabela cruzada laboratorio x resultado
    print("Gerando tabela cruzada laboratório x resultado...")
    tab_cruz2 = tabela_cruzada(df, "laboratorio", "resultado")
    tab_cruz2.to_csv(os.path.join(PASTA_TABELAS, "07_cruzamento_laboratorio_resultado.csv"))
    print(tab_cruz2.to_string())
    print()

    # 8. Taxa de positividade por patógeno e laboratório
    print("Calculando taxas de positividade...")
    taxa_pat = taxa_positividade_por_grupo(df, "patogeno")
    taxa_lab = taxa_positividade_por_grupo(df, "laboratorio")
    taxa_pat.to_csv(os.path.join(PASTA_TABELAS, "08_taxa_positividade_patogeno.csv"), index=False)
    taxa_lab.to_csv(os.path.join(PASTA_TABELAS, "09_taxa_positividade_laboratorio.csv"), index=False)
    print("\n-- Taxa de positividade por patógeno --")
    print(taxa_pat.to_string(index=False))
    print("\n-- Taxa de positividade por laboratório --")
    print(taxa_lab.to_string(index=False))
    print()

    # 9. Exportar todas as tabelas para um único ficheiro Excel (multi-folha)
    print("Exportando todas as tabelas para Excel (multi-folha)...")
    caminho_excel = os.path.join(PASTA_TABELAS, "relatorio_estatisticas.xlsx")
    with pd.ExcelWriter(caminho_excel, engine="openpyxl") as writer:
        tab_geral.to_excel(writer, sheet_name="Geral", index=False)
        tab_patogeno.to_excel(writer, sheet_name="Por Patogeno", index=False)
        tab_lab.to_excel(writer, sheet_name="Por Laboratorio", index=False)
        tab_resultado.to_excel(writer, sheet_name="Por Resultado", index=False)
        tabela_frequencias(df, "patogeno").to_excel(writer, sheet_name="Freq Patogeno", index=False)
        tabela_frequencias(df, "resultado").to_excel(writer, sheet_name="Freq Resultado", index=False)
        tabela_frequencias(df, "laboratorio").to_excel(writer, sheet_name="Freq Laboratorio", index=False)
        tabela_frequencias(df, "qualidade_amostra").to_excel(writer, sheet_name="Freq Qualidade", index=False)
        tab_cruz1.to_excel(writer, sheet_name="Cruz Patogeno-Resultado")
        tab_cruz2.to_excel(writer, sheet_name="Cruz Lab-Resultado")
        taxa_pat.to_excel(writer, sheet_name="Positividade Patogeno", index=False)
        taxa_lab.to_excel(writer, sheet_name="Positividade Lab", index=False)
    print(f"Ficheiro Excel guardado em: {caminho_excel}")

    print("\nAnálise estatística concluída com sucesso.")
    return df


if __name__ == "__main__":
    executar_analise()
