import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

def calcular_metricas(tp, tn, fp, fn):
    total = tp + tn + fp + fn
    acuracia = (tp + tn) / total if total else 0
    precisao = tp / (tp + fp) if (tp + fp) else 0
    recall = tp / (tp + fn) if (tp + fn) else 0
    especificidade = tn / (tn + fp) if (tn + fp) else 0
    f1 = 2 * (precisao * recall) / (precisao + recall) if (precisao + recall) else 0

    return {
        "Acurácia": round(acuracia, 4),
        "Precisão": round(precisao, 4),
        "Recall": round(recall, 4),
        "Especificidade": round(especificidade, 4),
        "F1-Score": round(f1, 4)
    }

def simular_custos(tp, tn, fp, fn, custo_fp=50, custo_fn=500):
    custo_total = (fp * custo_fp) + (fn * custo_fn)
    return {
        "Custo FP": fp * custo_fp,
        "Custo FN": fn * custo_fn,
        "Custo Total": custo_total
    }

def plotar_custos(custos, output_dir):
    labels = ["Custo FP", "Custo FN"]
    valores = [custos["Custo FP"], custos["Custo FN"]]

    plt.bar(labels, valores, color=["orange", "red"])
    plt.title("💰 Custos por Tipo de Erro")
    plt.ylabel("Valor em R$")
    plt.tight_layout()
    path = os.path.join(output_dir, "custos_barplot.png")
    plt.savefig(path, dpi=300)
    plt.close()
    print(f"📊 Gráfico de custos salvo em: {path}")

def plotar_metricas_radar(metricas, output_dir):
    labels = list(metricas.keys())
    valores = list(metricas.values())

    # Radar precisa de valores circulares
    valores += valores[:1]
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.plot(angles, valores, color="blue", linewidth=2)
    ax.fill(angles, valores, color="skyblue", alpha=0.4)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.set_title("📐 Métricas de Classificação", y=1.1)
    path = os.path.join(output_dir, "metricas_radar.png")
    plt.savefig(path, dpi=300)
    plt.close()
    print(f"📈 Gráfico de métricas salvo em: {path}")

def gerar_relatorio(tp, tn, fp, fn, custo_fp=50, custo_fn=500):
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    metricas = calcular_metricas(tp, tn, fp, fn)
    custos = simular_custos(tp, tn, fp, fn, custo_fp, custo_fn)

    df = pd.DataFrame([{
        **metricas,
        **custos,
        "VP": tp,
        "VN": tn,
        "FP": fp,
        "FN": fn
    }])

    print("📊 Relatório de Avaliação do Modelo:")
    print(df.T)

    # Exporta CSV
    csv_path = os.path.join(output_dir, "relatorio_metricas_custos.csv")
    df.to_csv(csv_path, index=False)
    print(f"📄 CSV salvo em: {csv_path}")

    # Gera gráficos
    plotar_custos(custos, output_dir)
    plotar_metricas_radar(metricas, output_dir)

    return df
