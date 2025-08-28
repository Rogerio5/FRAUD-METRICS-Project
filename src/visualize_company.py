import matplotlib.pyplot as plt
from sklearn.metrics import precision_recall_curve, average_precision_score

def visualize_company(y_true, y_scores, name="DetectorFraudeCorp", save_path="output/curva_precision_recall_empresa.png"):
    # Calcula precisão, recall e AP
    precision, recall, _ = precision_recall_curve(y_true, y_scores)
    ap = average_precision_score(y_true, y_scores)

    # Cria o gráfico
    plt.figure(figsize=(8, 6))
    plt.plot(recall, precision, label=f"{name} (AP = {ap:.2f})", color="#2a9d8f", linewidth=2)

    # Título mais descritivo
    plt.title(f"📈 Curva Precisão-Recall — {name}", fontsize=14, fontweight="bold", color="#264653")

    # Eixos
    plt.xlabel("Recall", fontsize=12)
    plt.ylabel("Precisão", fontsize=12)
    plt.xlim([0.0, 1.05])
    plt.ylim([0.0, 1.05])

    # Grid leve
    plt.grid(True, linestyle="--", alpha=0.3)

    # Legenda elegante
    plt.legend(loc="lower left", frameon=True, facecolor="white", edgecolor="#ccc")

    # Anotação destacando desempenho
    if ap == 1.0:
        plt.annotate("Desempenho Perfeito (AP = 1.00)",
                     xy=(0.95, 1.0), xytext=(0.6, 0.92),
                     arrowprops=dict(arrowstyle="->", color="green"),
                     fontsize=10, color="green")

    # Remove coordenadas interativas (se estiver usando notebooks)
    plt.gca().format_coord = lambda x, y: ""

    # Salva imagem
    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.close()

    print(f"✅ Curva Precisão-Recall salva em: {save_path}")
