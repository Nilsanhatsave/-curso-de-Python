"""
Projecto: Análise Estatística de Dados Laboratoriais (Valores Ct - PCR)
=========================================================================
Script de visualização: gera gráficos a partir dos dados laboratoriais.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

from analise_estatistica import carregar_dados

# ---------------------------------------------------------------------------
# Configuração
# ---------------------------------------------------------------------------
PASTA_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASTA_GRAFICOS = os.path.join(PASTA_BASE, "saidas", "graficos")
os.makedirs(PASTA_GRAFICOS, exist_ok=True)

sns.set_style("whitegrid")
plt.rcParams["figure.dpi"] = 110
PALETA = "Set2"


def guardar(fig, nome):
    caminho = os.path.join(PASTA_GRAFICOS, nome)
    fig.savefig(caminho, bbox_inches="tight")
    plt.close(fig)
    print(f"Gráfico guardado: {caminho}")


def grafico_histograma(df):
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(df["valor_ct"], bins=15, kde=True, color="#4C72B0", ax=ax)
    ax.axvline(df["valor_ct"].mean(), color="red", linestyle="--", label=f"Média = {df['valor_ct'].mean():.2f}")
    ax.axvline(df["valor_ct"].median(), color="green", linestyle="--", label=f"Mediana = {df['valor_ct'].median():.2f}")
    ax.set_title("Distribuição dos Valores Ct", fontsize=14, fontweight="bold")
    ax.set_xlabel("Valor Ct")
    ax.set_ylabel("Frequência")
    ax.legend()
    guardar(fig, "01_histograma_valor_ct.png")


def grafico_boxplot_patogeno(df):
    fig, ax = plt.subplots(figsize=(7, 5))
    sns.boxplot(data=df, x="patogeno", y="valor_ct", hue="patogeno", palette=PALETA, ax=ax, legend=False)
    sns.stripplot(data=df, x="patogeno", y="valor_ct", color="black", alpha=0.3, size=3, ax=ax)
    ax.set_title("Distribuição do Valor Ct por Patógeno", fontsize=14, fontweight="bold")
    ax.set_xlabel("Patógeno")
    ax.set_ylabel("Valor Ct")
    guardar(fig, "02_boxplot_por_patogeno.png")


def grafico_boxplot_laboratorio(df):
    fig, ax = plt.subplots(figsize=(7, 5))
    sns.boxplot(data=df, x="laboratorio", y="valor_ct", hue="laboratorio", palette=PALETA, ax=ax, legend=False)
    sns.stripplot(data=df, x="laboratorio", y="valor_ct", color="black", alpha=0.3, size=3, ax=ax)
    ax.set_title("Distribuição do Valor Ct por Laboratório", fontsize=14, fontweight="bold")
    ax.set_xlabel("Laboratório")
    ax.set_ylabel("Valor Ct")
    guardar(fig, "03_boxplot_por_laboratorio.png")


def grafico_barras_frequencia(df, coluna, titulo, nome_arquivo):
    fig, ax = plt.subplots(figsize=(6, 5))
    contagem = df[coluna].value_counts()
    cores = sns.color_palette(PALETA, len(contagem))
    barras = ax.bar(contagem.index, contagem.values, color=cores)
    for barra in barras:
        altura = barra.get_height()
        ax.annotate(f"{int(altura)}", (barra.get_x() + barra.get_width() / 2, altura),
                    ha="center", va="bottom", fontweight="bold")
    ax.set_title(titulo, fontsize=14, fontweight="bold")
    ax.set_ylabel("Número de Amostras")
    guardar(fig, nome_arquivo)


def grafico_pizza_resultado(df):
    fig, ax = plt.subplots(figsize=(6, 6))
    contagem = df["resultado"].value_counts()
    cores = ["#55A868", "#C44E52"] if contagem.index[0] == "Positivo" else ["#C44E52", "#55A868"]
    ax.pie(contagem.values, labels=contagem.index, autopct="%1.1f%%", startangle=90,
           colors=cores, wedgeprops={"edgecolor": "white", "linewidth": 1.5})
    ax.set_title("Proporção de Resultados (Positivo vs Negativo)", fontsize=14, fontweight="bold")
    guardar(fig, "06_pizza_resultados.png")


def grafico_barras_empilhadas_cruzamento(df):
    tabela = pd.crosstab(df["patogeno"], df["resultado"])
    fig, ax = plt.subplots(figsize=(7, 5))
    tabela.plot(kind="bar", stacked=True, ax=ax, color=["#C44E52", "#55A868"])
    ax.set_title("Resultado do Teste por Patógeno", fontsize=14, fontweight="bold")
    ax.set_xlabel("Patógeno")
    ax.set_ylabel("Número de Amostras")
    ax.legend(title="Resultado")
    plt.xticks(rotation=0)
    guardar(fig, "07_barras_empilhadas_patogeno_resultado.png")


def grafico_evolucao_temporal(df):
    df_tempo = df.copy()
    df_tempo["semana"] = df_tempo["data_teste"].dt.to_period("W").apply(lambda r: r.start_time)
    serie_semanal = df_tempo.groupby("semana")["valor_ct"].mean()

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(serie_semanal.index, serie_semanal.values, marker="o", color="#4C72B0", linewidth=2)
    ax.set_title("Evolução Semanal do Valor Ct Médio", fontsize=14, fontweight="bold")
    ax.set_xlabel("Semana")
    ax.set_ylabel("Valor Ct Médio")
    fig.autofmt_xdate(rotation=45)
    guardar(fig, "08_evolucao_temporal.png")


def grafico_correlacao_qualidade(df):
    fig, ax = plt.subplots(figsize=(7, 5))
    ordem = ["Boa", "Media"] if set(["Boa", "Media"]).issubset(df["qualidade_amostra"].unique()) else None
    sns.violinplot(data=df, x="qualidade_amostra", y="valor_ct", hue="qualidade_amostra",
                    palette=PALETA, ax=ax, order=ordem, legend=False)
    ax.set_title("Valor Ct por Qualidade da Amostra", fontsize=14, fontweight="bold")
    ax.set_xlabel("Qualidade da Amostra")
    ax.set_ylabel("Valor Ct")
    guardar(fig, "09_violino_qualidade_amostra.png")


def grafico_heatmap_taxa_positividade(df):
    tabela = pd.crosstab(df["laboratorio"], df["patogeno"], values=(df["resultado"] == "Positivo"), aggfunc="mean") * 100
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.heatmap(tabela, annot=True, fmt=".1f", cmap="YlGnBu", cbar_kws={"label": "Taxa de Positividade (%)"}, ax=ax)
    ax.set_title("Taxa de Positividade (%) por Laboratório e Patógeno", fontsize=13, fontweight="bold")
    guardar(fig, "10_heatmap_taxa_positividade.png")


def grafico_painel_resumo(df):
    """Painel com 4 sub-gráficos resumindo o dataset (dashboard único)."""
    fig, axes = plt.subplots(2, 2, figsize=(13, 10))

    # Histograma
    sns.histplot(df["valor_ct"], bins=15, kde=True, color="#4C72B0", ax=axes[0, 0])
    axes[0, 0].set_title("Distribuição do Valor Ct")
    axes[0, 0].set_xlabel("Valor Ct")

    # Boxplot por patógeno
    sns.boxplot(data=df, x="patogeno", y="valor_ct", hue="patogeno", palette=PALETA, ax=axes[0, 1], legend=False)
    axes[0, 1].set_title("Valor Ct por Patógeno")

    # Pizza de resultados
    contagem = df["resultado"].value_counts()
    cores = ["#55A868", "#C44E52"] if contagem.index[0] == "Positivo" else ["#C44E52", "#55A868"]
    axes[1, 0].pie(contagem.values, labels=contagem.index, autopct="%1.1f%%", startangle=90, colors=cores)
    axes[1, 0].set_title("Proporção de Resultados")

    # Barras por laboratório
    contagem_lab = df["laboratorio"].value_counts()
    axes[1, 1].bar(contagem_lab.index, contagem_lab.values, color=sns.color_palette(PALETA, len(contagem_lab)))
    axes[1, 1].set_title("Amostras por Laboratório")
    axes[1, 1].set_ylabel("Número de Amostras")

    fig.suptitle("Painel Resumo - Dados Laboratoriais", fontsize=16, fontweight="bold")
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    guardar(fig, "11_painel_resumo.png")


def gerar_todos_graficos():
    print("A carregar dados...")
    df = carregar_dados()
    print("A gerar gráficos...\n")

    grafico_histograma(df)
    grafico_boxplot_patogeno(df)
    grafico_boxplot_laboratorio(df)
    grafico_barras_frequencia(df, "patogeno", "Número de Amostras por Patógeno", "04_barras_patogeno.png")
    grafico_barras_frequencia(df, "laboratorio", "Número de Amostras por Laboratório", "05_barras_laboratorio.png")
    grafico_pizza_resultado(df)
    grafico_barras_empilhadas_cruzamento(df)
    grafico_evolucao_temporal(df)
    grafico_correlacao_qualidade(df)
    grafico_heatmap_taxa_positividade(df)
    grafico_painel_resumo(df)

    print("\nTodos os gráficos foram gerados com sucesso.")


if __name__ == "__main__":
    gerar_todos_graficos()
