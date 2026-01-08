import csv
import matplotlib.pyplot as plt
from collections import defaultdict

ARQUIVO_CSV = "benchmark_results.csv"

def carregar_e_agrupar_dados():
   
    agrupado = defaultdict(lambda: {
        "tempo_classico": [], 
        "tempo_strassen": [], 
        "chamadas": [], 
        "tempo_split": []
    })
    
    with open(ARQUIVO_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            n = int(row["n"])
            agrupado[n]["tempo_classico"].append(float(row["tempo_classico_seg"]))
            agrupado[n]["tempo_strassen"].append(float(row["tempo_strassen_seg"]))
            agrupado[n]["chamadas"].append(int(row["chamadas_recursivas"]))
            agrupado[n]["tempo_split"].append(float(row["tempo_split_join_seg"]))
    
    
    tamanhos = sorted(agrupado.keys())
    resumo = {
        "n": tamanhos,
        "classico_medio": [sum(agrupado[n]["tempo_classico"])/len(agrupado[n]["tempo_classico"]) for n in tamanhos],
        "strassen_medio": [sum(agrupado[n]["tempo_strassen"])/len(agrupado[n]["tempo_strassen"]) for n in tamanhos],
        "chamadas_media": [sum(agrupado[n]["chamadas"])/len(agrupado[n]["chamadas"]) for n in tamanhos],
        "split_medio": [sum(agrupado[n]["tempo_split"])/len(agrupado[n]["tempo_split"]) for n in tamanhos],
    }
    return resumo

def gerar_grafico_tempo(dados):
    plt.figure()
    plt.plot(dados["n"], dados["classico_medio"], marker="o", label="Tradicional (O(n³))")
    plt.plot(dados["n"], dados["strassen_medio"], marker="s", label="Strassen (O(n^2.81))")
    plt.xlabel("Dimensão da Matriz (n x n)")
    plt.ylabel("Tempo de Execução (s)")
    plt.title("Comparação de Desempenho: Clássico vs Strassen")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.savefig("comparacao_tempo.png")
    plt.close()

def gerar_grafico_overhead(dados):
    plt.figure()
    plt.bar([str(n) for n in dados["n"]], dados["strassen_medio"], label="Tempo Total Strassen")
    plt.bar([str(n) for n in dados["n"]], dados["split_medio"], label="Overhead (Split/Join)")
    plt.xlabel("Dimensão da Matriz (n x n)")
    plt.ylabel("Tempo (s)")
    plt.title("Impacto do Split/Join no Algoritmo de Strassen")
    plt.legend()
    plt.tight_layout()
    plt.savefig("overhead_strassen.png")
    plt.close()

def gerar_grafico_chamadas(dados):
    plt.figure()
    plt.plot(dados["n"], dados["chamadas_media"], marker="^", color="green", linestyle="--")
    plt.xlabel("Dimensão da Matriz (n x n)")
    plt.ylabel("Número de Chamadas Recursivas")
    plt.title("Crescimento de Chamadas no Strassen")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("chamadas_recursivas.png")
    plt.close()

if __name__ == "__main__":
    try:
        dados = carregar_e_agrupar_dados()
        gerar_grafico_tempo(dados)
        gerar_grafico_overhead(dados)
        gerar_grafico_chamadas(dados)
        print("Gráficos gerados com sucesso: comparacao_tempo.png, overhead_strassen.png e chamadas_recursivas.png")
    except FileNotFoundError:
        print(f"Erro: O arquivo {ARQUIVO_CSV} não foi encontrado. Execute o benchmark primeiro.")