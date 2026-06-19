"""
Script principal do projecto.
Executa, por ordem: análise estatística (tabelas) + geração de gráficos.

Uso:
    python3 src/main.py
"""

from analise_estatistica import executar_analise
from graficos import gerar_todos_graficos


def main():
    print("=" * 70)
    print(" PROJECTO: ANÁLISE ESTATÍSTICA DE DADOS LABORATORIAIS (PCR / Ct) ")
    print("=" * 70)
    print()

    print(">>> ETAPA 1: Medidas estatísticas e tabelas\n")
    executar_analise()

    print("\n" + "=" * 70)
    print(">>> ETAPA 2: Geração de gráficos\n")
    gerar_todos_graficos()

    print("\n" + "=" * 70)
    print("Pipeline concluído. Verifique a pasta 'saidas/' para:")
    print("  - saidas/tabelas/   -> ficheiros CSV e Excel")
    print("  - saidas/graficos/  -> ficheiros PNG")
    print("=" * 70)


if __name__ == "__main__":
    main()
