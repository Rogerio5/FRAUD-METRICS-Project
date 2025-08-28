import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from src.metrics import ConfusionMatrix, cost

def simular_custos(cm: ConfusionMatrix, fp_range=(5, 55, 10), fn_range=(5, 55, 10)) -> str:
    resultados = []

    # Garante que a pasta de saída existe
    os.makedirs("output", exist_ok=True)

    # Simulação de custos
    for cost_fp in range(*fp_range):
        for cost_fn in range(*fn_range):
            total = cost(cm, cost_fp, cost_fn)
            resultados.append({
                "Custo FP": cost_fp,
                "Custo FN": cost_fn,
                "Custo Total": total
            })

    # Cria DataFrame com os resultados
    df = pd.DataFrame(resultados)

    # 🔥 Exporta os dados simulados para CSV
    df.to_csv("output/simulacao_custos.csv", index=False)

    # 🔥 Gera o heatmap
    pivot = df.pivot(index="Custo FN", columns="Custo FP", values="Custo Total")
    plt.figure(figsize=(10, 6))
    sns.heatmap(pivot, annot=True, fmt=".0f", cmap="YlOrBr")
    plt.title("💸 Simulação de Custo Total")
    plt.xlabel("Custo Falso Positivo (FP)")
    plt.ylabel("Custo Falso Negativo (FN)")
    plt.tight_layout()
    plt.savefig("output/simulacao_custos.png", dpi=300)
    plt.close()

    # Mensagens de confirmação
    print("📈 Gráfico salvo em: output/simulacao_custos.png")
    print("📊 CSV salvo em: output/simulacao_custos.csv")

    # Retorna os 5 cenários mais econômicos
    top5 = df.sort_values("Custo Total").head(5)
    return top5.to_string(index=False)
