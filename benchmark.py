# benchmark.py
import csv
import random
from time import perf_counter

from classic import multiply_traditional
from strassen import multiply_strassen, reset_strassen_stats, get_strassen_stats


def gerar_matriz(n, rng, minimo, maximo):
    return [[rng.randint(minimo, maximo) for _ in range(n)] for _ in range(n)]


def medir_tempo(func, *args, **kwargs):
    t0 = perf_counter()
    resultado = func(*args, **kwargs)
    t1 = perf_counter()
    return (t1 - t0), resultado


def main():
    # >>> CONFIG DO BENCHMARK 
    tamanhos = [64, 128, 256, 512]     # pode adicionar mais: 1024 etc 
    repeticoes = 3                     # quantas vezes roda cada tamanho
    seed_base = 42                   
    minimo = 0
    maximo = 10

    arquivo_saida = "benchmark_results.csv"

    colunas = [
        "n",
        "repeticao",
        "seed",
        "tempo_classico_seg",
        "tempo_strassen_seg",
        "chamadas_recursivas",
        "tempo_split_join_seg",
    ]

    resultados = []

    for n in tamanhos:
        for rep in range(1, repeticoes + 1):
            seed = seed_base + (n * 1000) + rep
            rng = random.Random(seed)

            A = gerar_matriz(n, rng, minimo, maximo)
            B = gerar_matriz(n, rng, minimo, maximo)

            tempo_classico, C_classico = medir_tempo(multiply_traditional, A, B)

            reset_strassen_stats()
            tempo_strassen, C_strassen = medir_tempo(multiply_strassen, A, B)
            calls, split_join = get_strassen_stats()

            if C_classico != C_strassen:
                raise RuntimeError(f"ERRO: resultados diferentes em n={n} (rep={rep})")

            linha = {
                "n": n,
                "repeticao": rep,
                "seed": seed,
                "tempo_classico_seg": tempo_classico,
                "tempo_strassen_seg": tempo_strassen,
                "chamadas_recursivas": calls,
                "tempo_split_join_seg": split_join,
            }
            resultados.append(linha)

            print(
                f"n={n} rep={rep}/{repeticoes} | "
                f"classico={tempo_classico:.6f}s | "
                f"strassen={tempo_strassen:.6f}s | "
                f"calls={calls} | "
                f"split+join={split_join:.6f}s"
            )

    # Salvar CSV
    with open(arquivo_saida, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=colunas)
        writer.writeheader()
        writer.writerows(resultados)

    print(f"\nOK! Resultados salvos em: {arquivo_saida}")


if __name__ == "__main__":
    main()
